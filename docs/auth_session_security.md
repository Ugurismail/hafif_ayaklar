# Authentication Session Security

Date: 2026-09-28. Branch: codex/oturum-guvenligi-guncel. Base: main b30a8ae.
Status: locally verified, not pushed or deployed.
Original patch: 5b4fad9 on codex/oturum-guvenligi, reviewed and reapplied without
replacing later main changes (including day navigation and notification badges).

## Findings and Scope

- SEC-10 (new, P1): the login template stored the entered password and username
  in localStorage when remember-me was selected. This is a source-confirmed
  credential exposure risk, not evidence that credentials were stolen.
- SEC-08: GET /logout/ changed the session; login ignored the intended return
  URL. CSRF middleware was already enabled and remains enabled.
- SEC-07 rate limiting is still open. The production snapshot supplied by the
  user uses LocMemCache; this is not shared across WSGI workers. Request IP
  headers and edge protections have not been verified for abuse enforcement.
  These assumptions must not silently become an IP-based lockout policy.

## Changes

- Removed password/username localStorage reads and writes from login.
- A small first script in the shared base template removes only savedPassword
  and savedUsername. It never reads their values, logs them or sends them to a
  server. Unrelated preferences and drafts are preserved. Disabled storage
  does not prevent login. This runs for anonymous and signed-in visitors.
- Remember-me continues to control the existing session expiry: browser-close
  without it, 14 days with it. Native password-manager autocomplete hints are
  provided instead of application-managed plaintext credentials.
- Logout requires POST. Desktop and mobile menus submit ordinary forms with
  CSRF tokens; GET/HEAD return 405 without logging out. Session invalidation
  still uses Django's existing logout implementation.
- Login retains the validated next URL across failed attempts and success.
  Only Django-validated same-host destinations are allowed; HTTPS requests
  cannot redirect to HTTP. Unsafe destinations fall back to the homepage.
  POST next takes precedence over the query string. Template escaping remains
  enabled, and HttpResponseRedirect avoids resolving untrusted route names.
- Login/logout responses are marked non-cacheable. Login accepts GET/POST only
  and marks its password POST parameter sensitive for Django error reporting.
- No model, migration, requirements, proxy, database or production-env changes.

## Verification

### Current main integration (2026-09-28)

- 15 focused Django tests passed. Added coverage for anonymous session rotation,
  retained session preferences, invalidation/replay of the old logout cookie,
  inactive accounts and unsupported login methods.
- Full SQLite suite: 750 discovered, 745 passed, 5 existing row-lock tests
  skipped, 19.461 seconds. This run does not validate MySQL concurrency.
- 13 Node tests passed: credential cleanup, entry reference clipboard and
  notification polling. Migration check reports no changes.
- In-app browser against an isolated synthetic SQLite database: remember-me
  login to /notifications/, desktop menu logout via POST, guest menu afterward,
  and a protected page requiring login again. Menu screenshot inspected.
  No production data or credentials were used. The isolated server was stopped
  after testing. Mobile form structure is covered by the current Django test;
  the earlier mobile visual check below has not been repeated in this run.
- No plaintext credential reads/writes or GET logout links remain in templates.
  The shared cleanup is remove-only; Node coverage verifies that unrelated
  draft/theme storage is retained and inaccessible storage does not break it.

### Original patch validation (2026-09-20)

- Eleven Django regression tests first demonstrated the missing protections
  (nine failures including subtests), then passed after implementation.
- Full SQLite suite: 680 discovered, 675 passed, 5 MySQL concurrency tests
  skipped, 18.652 seconds. Those concurrency tests passed in an earlier MySQL
  run; this patch does not change database mutation/concurrency logic.
- Three new Node tests cover remove-only cleanup, preserving unrelated state,
  inaccessible storage and repeated visits. All 11 Node tests pass including
  the eight existing download tests.
- Chrome/Playwright at 1440px and 390px with an isolated local DB/test account:
  synthetic old credentials removed, unrelated preference retained, password
  field not populated by application code, remember-me login returned to the
  chosen draft page, logout GET rejected, menu logout POST succeeded with
  real CSRF, and signed-in menu disappeared. Screenshots inspected.
- makemigrations --check --dry-run and git diff --check passed. No production
  account, password, localStorage values or live attack traffic were inspected.

## Rollout and Limits

After separate publication approval: pull main in the PythonAnywhere Web
virtualenv, collectstatic, check, Web Reload. No migration or pip install is
required for this patch. Confirm login with/without remember-me, a protected
page's return URL, and desktop/mobile logout.

Cleanup applies when an updated page executes on each browser/origin. It cannot
erase offline browsers, old cached pages, disabled-JavaScript storage, another
origin's storage or previously copied credentials. Clearing these two keys
does not clear the browser's own password manager or invalidate active server
sessions. No breach or universal remediation is claimed. A credential-reset
or user-notification decision remains separate if exposure evidence emerges.

Next: verify a shared storage strategy and trusted client-IP boundary before
SEC-07 rate limiting; account-plus-IP bounds must not allow arbitrary account
lockout, must expire, and need parallel-worker tests. SEC-02 supported Django
upgrade is still open. This patch is not a replacement for either workstream.

## Primary References

- [OWASP HTML5 storage guidance](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html#local-storage)
  explains why sensitive credentials should not be kept in localStorage.
- [Django HTTP decorators](https://docs.djangoproject.com/en/5.2/topics/http/decorators/)
  documents method restrictions and cache-control decorators.
- [Django authentication](https://docs.djangoproject.com/en/5.2/topics/auth/default/)
  documents login/logout and return-URL behavior. Runtime remains 4.2.2 in
  this patch; no supported-version upgrade is implied by the reference URL.
