# Delivery checks and project boundary

This is a static demo website with HTML, CSS, JavaScript and local logo assets. Preserve its existing lifecycle and source ownership.

The legacy workflow `sync-from-tourops.yml` previously fetched an old design branch, hard-reset the checkout and force-pushed `main` on a schedule. That destructive integration path is retired. Its manual replacement only reports a source diff; it cannot push. Any adopted changes go through a reviewed PR and the same checks as other work. Do not reenable the schedule, force-push, or import the legacy branch automatically.

The inspected Vercel project `lone-star-shine` (`prj_csVVe8GzgfExxV9TD7yD8KJWfG5e`) is linked to this repository's `main`. For an authorized release, confirm the actual target and deployed SHA, then check the changed user flow. This governance change does not authorize customer messaging, new offers or reactivation of another demo.

Follow [SOFTWARE_DELIVERY.md](../SOFTWARE_DELIVERY.md) and the adapted skill for proportional brainstorming, planning, independent final-diff review and authorized delivery.

## Enumerated source verification

- Supported local resources (tracked paths): script/img/source/video/audio/iframe src; video poster; link href for ASCII-case-insensitive stylesheet/icon/preload/modulepreload; img/source srcset; CSS url(...) and quoted @import in lowercase .css, style blocks and style attributes.

- Supported anchors: #id and explicit local .html#id targets and IDs. Supported syntax: inline classic/module scripts, lowercase .js/.mjs sources and their local static import/re-export graph, and FunctionBody syntax for the finite handler list below. Script/style EOF and repository path escapes are rejected; any base[href] is unsupported and fails closed.

- Handler allowlist (HTML GlobalEventHandlers snapshot, not all DOM handlers): onabort onauxclick onbeforeinput onbeforematch onbeforetoggle onblur oncancel oncanplay oncanplaythrough onchange onclick onclose oncommand oncontextlost oncontextmenu oncontextrestored oncopy oncuechange oncut ondblclick ondrag ondragend ondragenter ondragleave ondragover ondragstart ondrop ondurationchange onemptied onended onerror onfocus onformdata oninput oninvalid onkeydown onkeypress onkeyup onload onloadeddata onloadedmetadata onloadstart onmousedown onmouseenter onmouseleave onmousemove onmouseout onmouseover onmouseup onpaste onpause onplay onplaying onprogress onratechange onreset onresize onscroll onscrollend onsecuritypolicyviolation onseeked onseeking onselect onslotchange onstalled onsubmit onsuspend ontimeupdate ontoggle onvolumechange onwaiting onwebkitanimationend onwebkitanimationiteration onwebkitanimationstart onwebkittransitionend onwheel

- Unverified extensions: query-only same-page fragments; manifest links; track/object/embed/image-input resource attributes; CSS image-set string candidates; nonlowercase/extensionless or other local script/dependency filenames; other event-handler families; bare/import-map/dynamic module resolution; plain navigation and rewritten routes.

- Limits: lowercase .html/.css/.js/.mjs source loading only; bounded lexical CSS/HTML checks, not full parser/error recovery, module linking/evaluation, image selection/fetch, DOM execution or production/user-flow proof. Use focused verification or a scoped extension for an outcome relying on an unverified surface.

The checker prints this same contract in `--help` and after successful supported checks. An `UNVERIFIED` diagnostic identifies an observed surface outside that contract; it is not a syntax/resource pass for that surface. Ordinary unfamiliar attributes such as `onboarding` are inert data and are not rejected as handlers. The finite handler list is sourced from the [HTML GlobalEventHandlers IDL snapshot](https://html.spec.whatwg.org/multipage/webappapis.html#handler-globaleventhandlers), October 18, 2026; other standards and Window-only handlers are not claimed.

A changed outcome relying on an unverified extension needs focused verification or a separately scoped checker improvement. This does not require Todd to choose engineering tactics. No new dependency, universal unknown-HTML ban, full browser validator or production behavior claim is introduced.
