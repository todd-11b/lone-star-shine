# Delivery checks and project boundary

This is a static demo website with HTML, CSS, JavaScript and local logo assets. Preserve its existing lifecycle and source ownership.

The `delivery-checks` candidate verifies local resources, same-page fragment targets and inline/external JavaScript syntax. It needs no package installation or provider credentials and executes no app code. Require it only after its first green hosted run. Changed interactions also need focused safe browser verification.

The legacy workflow `sync-from-tourops.yml` previously fetched an old design branch, hard-reset the checkout and force-pushed `main` on a schedule. That destructive integration path is retired. Its manual replacement only reports a source diff; it cannot push. Any adopted changes go through a reviewed PR and the same checks as other work. Do not reenable the schedule, force-push, or import the legacy branch automatically.

The inspected Vercel project `lone-star-shine` (`prj_csVVe8GzgfExxV9TD7yD8KJWfG5e`) is linked to this repository's `main`. For an authorized release, confirm the actual target and deployed SHA, then check the changed user flow. This governance change does not authorize customer messaging, new offers or reactivation of another demo.

Follow [SOFTWARE_DELIVERY.md](../SOFTWARE_DELIVERY.md) and the adapted skill for proportional brainstorming, planning, independent final-diff review and authorized delivery.
