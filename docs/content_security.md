# Content Interaction Security

Date: 2026-09-12. Branch: codex/icerik-iyilestirmeleri. Base: origin/main 93841c7.
Status: implemented locally; not committed, pushed or deployed.
The user confirmed that the previous retirement/attendance release works in
production. That confirmation does not verify this new patch.

## Changes

- Report return URLs must pass Django's host/scheme validation. HTTPS requests
  cannot redirect to HTTP. Invalid-reason redirects URL-encode query values,
  preserving local query strings and fragments without parameter injection.
- Vote, save and collection-options endpoints accept only existing Question or
  Answer targets, not arbitrary Django ContentTypes. Invalid IDs and values are
  rejected before mutation. Vote/save require POST; CSRF remains enabled.
- Vote changes and counter updates share one transaction. A target-row lock
  serializes votes for that target on databases supporting select_for_update.
  Counter-only updates avoid overwriting content or changing edit timestamps.
- Saved-list lookup is owner-only, including the username query parameter.
  Saved-list and collection-options responses carry private/no-store headers.
  Legacy unsupported or missing saved targets are ignored, not deleted.
- Collection selections and names are validated before save mutations. Invalid
  or foreign IDs no longer silently erase current selections. Link changes and
  new saves roll back together on failure. Explicit unsave is idempotent; the
  existing implicit toggle and explicit save actions retain their contracts.
- Saved-list content is fetched in bulk, removing per-item content/parent
  queries. A warm-ContentType regression test verifies three queries for a
  mixed list of nine saved items. This is not a production latency benchmark.

## Verification

- Wrote initial regression tests before implementation and observed failures.
- Final full suite including content/export changes, on local Python 3.11 /
  Django 4.2.2 / isolated SQLite: 643 discovered, 641 passed, 2 skipped,
  18.737 seconds, with all updated export dependencies installed together.
- 25 new tests: ownership, target validation, external redirects, normal
  question/answer usage, independent voters, CSRF rejection and acceptance,
  timestamp preservation, rollback, stale saves and bounded query count.
- Two parallel-vote tests are deliberately skipped without row-lock support.
  They cover different voters and simultaneous toggles by the same voter.
  Both passed separately with all 25 security tests on an isolated MySQL
  8.0.46 Docker database (PyMySQL test driver), in 0.847 seconds, no skips.
  This verifies local InnoDB concurrency, not the live deployment, driver or
  production load. Never run the test runner against the live database.
- manage.py check, makemigrations --check --dry-run and git diff --check passed.
  The security patch has no model or migration changes. The accompanying
  content/export work has separate template, static and dependency changes.
- No live attack probes or production writes. Browser checks covered the
  accompanying invitation-copy, outline and diagram preview work, not a full
  security end-to-end audit.

## Rollout and Remaining Work

Review and explicitly approve publication before merging/pushing. After an
approved push, use the PythonAnywhere Web virtualenv, pull main, run check and
Web Reload. This patch itself requires no migration or dependency upgrade.
The accompanying export work adds resvg-py, WeasyPrint and pypdf and updates
Bleach/tinycss2. Bleach 6.4.0 fixes sanitization issues and removes the older
CSS dependency constraint, but Bleach is now unmaintained; choosing and
regression-testing a maintained sanitizer remains an audit item. See
content_export_improvements.md before deploying the combined branch.
Smoke-test vote/change/remove, save/new collection/change collection/remove,
own saved-list search and report return navigation with ordinary test accounts.

Do not merge the older general-review security branch wholesale: it contains
retired radio code, overlapping fixes and separate configuration changes.
This patch does not rotate keys, modify .env, enable MySQL strict mode or change
the Django version. Supported dependency upgrades, upload isolation, export
formula handling, login/invitation abuse controls and broader private-response
caching remain separate audit items. Other redirect handlers are not covered
by the report-specific fix. Passing these tests is not a claim that the whole
site is free of vulnerabilities.
