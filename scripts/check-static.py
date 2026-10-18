#!/usr/bin/env python3
"""Check static-site references and JavaScript syntax; never execute app code."""

import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit


def local_path(owner, value):
    url = urlsplit(value.strip())
    if url.scheme or url.netloc or not url.path:
        return None
    path = PurePosixPath(unquote(url.path))
    joined = path if path.is_absolute() else PurePosixPath(owner).parent / path
    parts = []
    for part in joined.parts:
        if part in ("", "/", "."):
            continue
        if part == "..":
            if not parts:
                raise ValueError(f"{owner}: resource escapes repository: {value}")
            parts.pop()
        else:
            parts.append(part)
    return "/".join(parts)


def strip_css_comments(content):
    # Ignore comments while preserving quoted and escaped comment markers.
    live = []
    quote = None
    index = 0
    while index < len(content):
        char = content[index]
        if char == "\\":
            live.append(content[index:index + 2])
            index += 2
            continue
        if quote:
            live.append(char)
            if char == quote:
                quote = None
        elif char in ("'", '"'):
            quote = char
            live.append(char)
        elif content.startswith("/*", index):
            close = content.find("*/", index + 2)
            if close < 0:
                break
            live.append(" ")
            index = close + 2
            continue
        else:
            live.append(char)
        index += 1
    return "".join(live)


def css_string(content, index):
    """Read one quoted CSS string, including escapes; never evaluate CSS."""
    quote = content[index]
    result = []
    index += 1
    while index < len(content):
        char = content[index]
        index += 1
        if char == quote:
            return "".join(result), index
        if char in "\n\r\f":
            return None, index  # An unescaped newline produces a bad string.
        if char != "\\":
            result.append(char)
            continue
        if index == len(content):
            break
        char = content[index]
        if char in "\n\r\f":
            index += 1
            if char == "\r" and index < len(content) and content[index] == "\n":
                index += 1
        elif char in "0123456789abcdefABCDEF":
            start = index
            while index < len(content) and index - start < 6 and content[index] in "0123456789abcdefABCDEF":
                index += 1
            code = int(content[start:index], 16)
            result.append(chr(code) if 0 < code <= 0x10ffff and not 0xd800 <= code <= 0xdfff else "\ufffd")
            if index < len(content) and content[index] in " \t\n\r\f":
                char = content[index]
                index += 1
                if char == "\r" and index < len(content) and content[index] == "\n":
                    index += 1
        else:
            result.append(char)
            index += 1
    return None, index


def css_resources(content):
    live = strip_css_comments(content)
    resources = []
    index = 0
    while index < len(live):
        if live[index] in ("'", '"'):
            _, index = css_string(live, index)
            continue
        if live[index] == "\\":
            index += 2
            continue
        if live[index:index + 4].lower() == "url(" and (index == 0 or not (live[index - 1].isalnum() or live[index - 1] in "_-\\")):
            start = index + 4
            while start < len(live) and live[start] in ASCII_SPACE:
                start += 1
            if start < len(live) and live[start] in ("'", '"'):
                resource, end = css_string(live, start)
                while end < len(live) and live[end] in ASCII_SPACE:
                    end += 1
                if resource is not None and end < len(live) and live[end] == ")":
                    resources.append(resource)
                    index = end + 1
                    continue
            else:
                match = re.match(r"url\(\s*(.*?)\s*\)", live[index:], re.IGNORECASE | re.DOTALL)
                if match:
                    resources.append(match[1])
                    index += match.end()
                    continue
        if live[index:index + 7].lower() == "@import":
            end = index + 7
            # A longer at-keyword such as @important is not @import.
            if end < len(live) and (live[end].isalnum() or live[end] in "_-\\"):
                index = end
                continue
            while end < len(live) and live[end] in " \t\n\r\f":
                end += 1
            if end < len(live) and live[end] in ("'", '"'):
                resource, index = css_string(live, end)
                if resource is not None:
                    resources.append(resource)
                continue
        index += 1
    return resources


ASCII_SPACE = " \t\n\r\f"
SRCSET_FLOAT = re.compile(r"-?(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?x\Z")


def srcset_resources(content):
    """WHATWG srcset URL/descriptor parsing, without choosing an image or fetching."""
    resources = []
    position = 0
    while position < len(content):
        while position < len(content) and content[position] in ASCII_SPACE + ",":
            position += 1
        start = position
        while position < len(content) and content[position] not in ASCII_SPACE:
            position += 1
        url = content[start:position]
        if not url:
            break
        descriptors = []
        if url.endswith(","):
            url = url.rstrip(",")
        else:
            current = ""
            state = "descriptor"
            while True:
                char = content[position] if position < len(content) else None
                if char is None:
                    if current:
                        descriptors.append(current)
                    break
                if state == "parens":
                    current += char
                    if char == ")":
                        state = "descriptor"
                elif char == ",":
                    if current:
                        descriptors.append(current)
                    position += 1
                    break
                elif char in ASCII_SPACE:
                    if current:
                        descriptors.append(current)
                        current = ""
                    state = "after"
                else:
                    current += char
                    state = "parens" if char == "(" else "descriptor"
                position += 1
        width = density = height = False
        valid = True
        for descriptor in descriptors:
            if re.fullmatch(r"[0-9]+w", descriptor):
                valid &= not (width or density) and bool(descriptor[:-1].lstrip("0"))
                width = True
            elif SRCSET_FLOAT.fullmatch(descriptor):
                valid &= not (width or density or height) and float(descriptor[:-1]) >= 0
                density = True
            elif re.fullmatch(r"[0-9]+h", descriptor):
                valid &= not (height or density) and bool(descriptor[:-1].lstrip("0"))
                height = True
            else:
                valid = False
        if valid and (not height or width):
            resources.append(url)
    return resources


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.resources = []
        self.anchors = []
        self.links = []
        self.scripts = []
        self.external_scripts = []
        self.handlers = []
        self.script = None
        self.open_script_line = None
        self.style = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag in ("script", "img", "source", "video", "audio", "iframe") and attrs.get("src"):
            self.resources.append(attrs["src"])
        if tag in ("img", "source") and attrs.get("srcset"):
            self.resources.extend(srcset_resources(attrs["srcset"]))
        if tag == "video" and attrs.get("poster"):
            self.resources.append(attrs["poster"])
        if tag == "link" and set(attrs.get("rel", "").split()) & {"stylesheet", "icon", "preload", "modulepreload"} and attrs.get("href"):
            self.resources.append(attrs["href"])
        if tag == "a" and attrs.get("href", "").startswith("#") and len(attrs["href"]) > 1:
            self.anchors.append(unquote(attrs["href"][1:]))
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        self.resources.extend(css_resources(attrs.get("style", "")))
        if tag == "style":
            self.style = []
        for name, body in attrs.items():
            if name.startswith("on") and body is not None:
                self.handlers.append({"line": self.getpos()[0], "name": name, "body": body})
        if tag == "script":
            self.open_script_line = self.getpos()[0]
            kind = attrs.get("type", "").strip().lower()
            if kind in ("", "module", "text/javascript", "application/javascript", "text/ecmascript", "application/ecmascript"):
                grammar = "module" if kind == "module" else "script"
                if attrs.get("src"):
                    self.external_scripts.append((attrs["src"], grammar))
                else:
                    self.script = {"line": self.getpos()[0], "kind": grammar, "parts": []}

    def handle_data(self, data):
        if self.script is not None:
            self.script["parts"].append(data)
        if self.style is not None:
            self.style.append(data)

    def handle_endtag(self, tag):
        if tag == "script":
            self.open_script_line = None
        if tag == "script" and self.script is not None:
            self.scripts.append(self.script)
            self.script = None
        if tag == "style" and self.style is not None:
            self.resources.extend(css_resources("".join(self.style)))
            self.style = None


def module_details(label, source):
    # Constructing a SourceTextModule parses only. Never link or evaluate it.
    parser = """
const source = require("node:fs").readFileSync(0, "utf8");
const module = new (require("node:vm").SourceTextModule)(source);
process.stdout.write(JSON.stringify(module.moduleRequests.map(request => request.specifier)));
"""
    result = subprocess.run(["node", "--experimental-vm-modules", "--eval", parser],
                            input=source, capture_output=True, text=True, timeout=10)
    if result.returncode:
        return f"{label}: JavaScript syntax invalid\n{result.stderr}", []
    return None, json.loads(result.stdout)


def javascript_error(label, source, kind="script"):
    if kind == "module":
        return module_details(label, source)[0]
    # vm.Script uses browser Script grammar, without CommonJS's implicit
    # function wrapper. Function construction parses handler FunctionBody
    # grammar (where return is legal) but never calls the resulting function.
    parser = """
const source = require("node:fs").readFileSync(0, "utf8");
if (process.argv[1] === "handler") new Function(source);
else new (require("node:vm").Script)(source);
"""
    result = subprocess.run(["node", "--eval", parser, kind],
                            input=source, capture_output=True, text=True, timeout=10)
    return f"{label}: JavaScript syntax invalid\n{result.stderr}" if result.returncode else None


def check_sources(tracked, sources):
    errors = []
    pages = {}
    external_kinds = {}
    for path, content in sources.items():
        if not path.endswith(".html"):
            continue
        page = Page()
        page.feed(content)
        page.close()
        pages[path] = page
        if page.open_script_line is not None:
            errors.append(f"{path}:{page.open_script_line}: unclosed script at EOF")
        if page.style is not None:
            errors.append(f"{path}: unclosed style at EOF")
        for reference, kind in page.external_scripts:
            try:
                resolved = local_path(path, reference)
            except ValueError:
                continue  # The resource check below reports this invalid path.
            if resolved is not None:
                external_kinds.setdefault(resolved, set()).add(kind)
    module_cache = {}

    def parsed_module(label, source):
        key = (label, source)
        if key not in module_cache:
            module_cache[key] = module_details(label, source)
        return module_cache[key]

    pending = [(path, path, content) for path, content in sources.items()
               if path.endswith(".mjs") or "module" in external_kinds.get(path, set())]
    for path, page in pages.items():
        pending.extend((path, f"{path}:{script['line']}", "".join(script["parts"]))
                       for script in page.scripts if script["kind"] == "module")
    seen = set()
    while pending:
        owner, label, source = pending.pop()
        if (label, source) in seen:
            continue
        seen.add((label, source))
        _, specifiers = parsed_module(label, source)
        for specifier in specifiers:
            # Bare/import-map, remote and dynamic requests are outside this
            # bounded local static-import/export-from graph.
            if not specifier.startswith(("./", "../", "/")):
                continue
            try:
                resolved = local_path(owner, specifier)
            except ValueError as error:
                errors.append(str(error))
                continue
            if resolved is None:
                continue
            if resolved not in tracked:
                errors.append(f"{owner}: missing tracked module {specifier} -> {resolved}")
            elif resolved in sources and resolved.endswith((".js", ".mjs")):
                external_kinds.setdefault(resolved, set()).add("module")
                pending.append((resolved, resolved, sources[resolved]))

    for path, content in sources.items():
        references = []
        if path.endswith(".html"):
            page = pages[path]
            references = page.resources
            for anchor in page.anchors:
                if anchor not in page.ids:
                    errors.append(f"{path}: missing anchor #{anchor}")
            for reference in page.links:
                # Check cross-page fragment links to explicit local HTML pages.
                # Ordinary navigation, rewritten routes and other media remain
                # outside this bounded anchor check.
                if not urlsplit(reference).fragment:
                    continue
                try:
                    target = local_path(path, reference)
                except ValueError as error:
                    errors.append(str(error))
                    continue
                if target is None or not target.endswith(".html"):
                    continue
                if target not in tracked:
                    errors.append(f"{path}: missing tracked HTML target {reference} -> {target}")
                elif target in pages:
                    fragment = unquote(urlsplit(reference).fragment)
                    if fragment and fragment not in pages[target].ids:
                        errors.append(f"{path}: missing anchor #{fragment} in {target}")
            for script in page.scripts:
                label, source = f"{path}:{script['line']}", "".join(script["parts"])
                error = parsed_module(label, source)[0] if script["kind"] == "module" else javascript_error(label, source)
                if error:
                    errors.append(error)
            for handler in page.handlers:
                error = javascript_error(f"{path}:{handler['line']} {handler['name']}", handler["body"], "handler")
                if error:
                    errors.append(error)
        elif path.endswith(".css"):
            references = css_resources(content)
        elif path.endswith((".js", ".mjs")):
            kinds = external_kinds.get(path, {"module" if path.endswith(".mjs") else "script"})
            for kind in sorted(kinds):
                error = parsed_module(path, content)[0] if kind == "module" else javascript_error(f"{path} ({kind})", content, kind)
                if error:
                    errors.append(error)
        for reference in references:
            try:
                resolved = local_path(path, reference)
            except ValueError as error:
                errors.append(str(error))
                continue
            if resolved is not None and resolved not in tracked:
                errors.append(f"{path}: missing tracked resource {reference} -> {resolved}")
    return errors


def main():
    tracked = set(subprocess.check_output(["git", "ls-files", "-z"]).decode().split("\0")) - {""}
    if "index.html" not in tracked:
        raise SystemExit("Root index.html must be tracked.")
    sources = {path: Path(path).read_text() for path in sorted(tracked) if path.endswith((".html", ".css", ".js", ".mjs"))}
    errors = check_sources(tracked, sources)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Static checks passed: {len(sources)} HTML/CSS/JS files; local resources, anchors and inline/external JavaScript and event-handler syntax.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
