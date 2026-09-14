# Download Progress and PDF Follow-Up

Date: 2026-09-14. Branch: codex/davet-guvenligi, following a8b712d.
Local implementation; not pushed or deployed.

## User-Reported Production Evidence

The user pulled main d13dc0b and successfully installed its requirements in the
actual Web virtualenv. WeasyPrint reports version 70.0, Python 3.10.12 and Pango
15006. collectstatic and Django check completed successfully. This confirms
library loading, not every document conversion scenario.

The production PDF endpoint returned the application's 60-second timeout error.
The same selection downloads as Word, approximately 20 MB. Entry/page count and
the actual document are not available for reproduction. The production timeout
is still OPEN; local synthetic results do not close it.

## Changes

- Replaced top-level form navigation with same-origin POST fetch, retaining
  CSRF, explicit selections, order, whole-archive and root-only scope rules.
- The download dialog stays open with an indeterminate status until the entire
  attachment is received and handed to the browser through a download link.
  It does not claim that the user has saved the file to disk.
- Duplicate requests are blocked while pending, selection controls are inert,
  and Escape/backdrop/close cannot silently hide the pending status. The explicit
  stop-waiting button aborts the client request and restores controls/selections.
  It does not promise to kill server work already executing under WSGI.
- Timeout, network, authentication, empty-file and unexpected HTML responses
  remain in the dialog; server text is assigned as text, never injected as HTML.
  No automatic retries or conversion to another format are performed.
- All four formats use reversed Django URLs. Document filenames use Django's
  Content-Disposition helper and the client decodes Unicode filenames safely.
- PDF projection caches computed paragraph CSS per document/style/direct-format
  combination. Direct paragraph overrides remain distinct. Single-note pages
  that already have correct symbols no longer trigger a redundant layout pass.
- The 60-second native-worker limit, 32 MiB DOCX bound, asset allowlist and Linux
  resource limits remain unchanged. Word layout/content has not been simplified.

## Verification

- Full isolated SQLite suite: 666 discovered, 661 passed, 5 skipped, 18.195s.
  The five row-lock tests passed previously within 44 MySQL tests; this patch
  does not change database mutation code.
- Eight Node tests pass: four formats, POST/CSRF/signal preservation, waiting
  for response body, Unicode names, error/redirect/HTML rejection, empty files,
  abort/network propagation, and no automatic retry.
  Run: `node --test tests/js/entry_download.test.cjs` (Node 18+).
- Local Chrome/Playwright at 1440px and 390px: delayed response keeps the notice
  visible; duplicate click sends one request; native download event occurs;
  Unicode name is preserved; URL never changes; 503/HTML/cancel/retry work and
  selection survives. Pending-footer screenshots were inspected, with no
  horizontal overflow. Safari/Firefox/mobile-native downloads remain untested.
- PDF tests preserve diagrams, notes, bibliography, page-local symbols, direct
  formatting and long-note checks. A cache test reduces CSS computations for
  31 paragraphs to two and verifies distinct indentation.
- Synthetic 300-entry/1200-paragraph cProfile run: 6.147s before vs 4.400s after,
  on the same local machine. Single-sample measurement, not a production SLA.
- A separate synthetic image-heavy DOCX of 20.34 MiB produced an 18-page PDF
  of 20.31 MiB in 1.534s through the bounded worker. This is not the user's
  document and does not show that all 20 MB exports finish on PythonAnywhere.

## Remaining Limits / Next Step

The fetch workflow buffers the complete attachment as a Blob before browser
handoff. It is suitable for the tested scope but is not a streaming/background
export queue, nor an unlimited-size guarantee. Object URLs are released after
handoff; no files are uploaded to a third-party conversion service.

Re-test the user's real selection after an approved deployment, or reproduce
with a user-provided document before claiming its timeout is fixed. If it still
exceeds the request budget, design a persistent export job with owner-only
status/download, bounded concurrency, expiry/cleanup and a verified host worker
mechanism. Do not simply extend WSGI timeouts or start an unreliable in-process
background thread. Request preparation before the PDF subprocess is still a
separate workload needing total-book budgets.
