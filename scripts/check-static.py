#!/usr/bin/env python3
"""Check static-site references and JavaScript syntax; never execute app code."""

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


def css_resources(content):
    return [match[1] for match in re.findall(r"url\(\s*(['\"]?)(.*?)\1\s*\)", content, re.DOTALL)]


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.resources = []
        self.anchors = []
        self.scripts = []
        self.external_scripts = []
        self.handlers = []
        self.script = None
        self.style = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag in ("script", "img", "source", "video", "audio", "iframe") and attrs.get("src"):
            self.resources.append(attrs["src"])
        if tag == "video" and attrs.get("poster"):
            self.resources.append(attrs["poster"])
        if tag == "link" and set(attrs.get("rel", "").split()) & {"stylesheet", "icon", "preload", "modulepreload"} and attrs.get("href"):
            self.resources.append(attrs["href"])
        if tag == "a" and attrs.get("href", "").startswith("#") and len(attrs["href"]) > 1:
            self.anchors.append(unquote(attrs["href"][1:]))
        self.resources.extend(css_resources(attrs.get("style", "")))
        if tag == "style":
            self.style = []
        for name, body in attrs.items():
            if name.startswith("on") and body is not None:
                self.handlers.append({"line": self.getpos()[0], "name": name, "body": body})
        if tag == "script":
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
        if tag == "script" and self.script is not None:
            self.scripts.append(self.script)
            self.script = None
        if tag == "style" and self.style is not None:
            self.resources.extend(css_resources("".join(self.style)))
            self.style = None


def javascript_error(label, source, kind="script"):
    if kind == "module":
        command = ["node", "--input-type=module", "--check"]
    else:
        # vm.Script uses browser Script grammar, without CommonJS's implicit
        # function wrapper. Function construction parses handler FunctionBody
        # grammar (where return is legal) but never calls the resulting function.
        parser = """
const source = require("node:fs").readFileSync(0, "utf8");
if (process.argv[1] === "handler") new Function(source);
else new (require("node:vm").Script)(source);
"""
        command = ["node", "--eval", parser, kind]
    result = subprocess.run(command, input=source, capture_output=True, text=True, timeout=10)
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
        pages[path] = page
        for reference, kind in page.external_scripts:
            try:
                resolved = local_path(path, reference)
            except ValueError:
                continue  # The resource check below reports this invalid path.
            if resolved is not None:
                external_kinds.setdefault(resolved, set()).add(kind)
    for path, content in sources.items():
        references = []
        if path.endswith(".html"):
            page = pages[path]
            references = page.resources
            for anchor in page.anchors:
                if anchor not in page.ids:
                    errors.append(f"{path}: missing anchor #{anchor}")
            for script in page.scripts:
                error = javascript_error(f"{path}:{script['line']}", "".join(script["parts"]), script["kind"])
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
                error = javascript_error(f"{path} ({kind})", content, kind)
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
