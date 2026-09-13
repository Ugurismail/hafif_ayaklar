# Invitation Quota Security

Date: 2026-09-13. Branch: codex/davet-guvenligi.
Base: local XLSX commit 438b20b, following published main d13dc0b.
This invitation patch and its XLSX parent are not pushed or deployed.

## Scope and Findings

SEC-07 is only partly addressed here: quota correctness, not login or
invitation endpoint rate limiting. Both /send-invitation/ and the owner's
profile invitation tab previously checked a previously loaded balance outside
the transaction. Concurrent requests could create more grants than the balance
funded. Their full-profile saves could also overwrite concurrent profile edits.

The profile invitation tab subtracted invitation count from an already debited
balance, showing an incorrect remaining quota. Invitation count and transferable
quota are different quantities; the existing quota transfer policy is preserved.

Other profile writes (theme save/reset, photo save/remove, excluded words) could
restore a stale quota. Those writes now persist only their own fields. Theme
reset's old assignment to the nonexistent `cemil` model field was removed; it
was not previously persisted. No theme redesign or permission change is included.

## Implementation

- Both creation views use core/invitations.py. A conditional database UPDATE
  reserves quota only if the current stored balance is sufficient. F-expression
  subtraction and code insertion share one transaction; insert failure rolls
  back the debit. Unrelated profile fields are never written by this operation.
- A positive integer grant is required, bounded by the portable signed integer
  range already supported by the existing PositiveIntegerField schema.
- The standalone page reloads its displayed quota from the database; the profile
  reads the stored remaining balance directly, without subtracting code count.
- Existing login/owner/CSRF checks remain. Normal GET requests do not issue codes.
- Signup's existing select_for_update lock is retained, not replaced. Tests
  verify one successful account for a shared code and rollback after signup
  failure, including created user/profile records and code state.

## Verification

- Regression tests failed before fixes for stale quota, unrelated profile
  overwrites, double subtraction and quota restoration from profile settings.
- 14 invitation tests cover both creation paths, quota transfers and rejection,
  owner/CSRF/anonymous access, code-insert rollback, signup failure, invalid or
  reused codes, and three database concurrency scenarios.
- Full isolated SQLite suite: 662 discovered, 657 passed, 5 skipped, 17.876s.
- Isolated MySQL 8.0.46: 44 tests (invitations, content interaction security and
  XLSX security) passed in 1.965s with no skips. This includes all five tests
  SQLite skips: two vote tests and three invitation/signup concurrency tests.
- Concurrency tests synchronize validated requests before mutation, use separate
  connections, and test mixed creation endpoints and grants larger than one.
- MySQL used a disposable local container and PyMySQL compatibility driver.
  Production data, credentials and network endpoints were not used. This is
  not a production load benchmark or proof of the live driver/configuration.
- Existing MySQL slug-length warning remains; it is unrelated to this patch.
- makemigrations --check --dry-run: no changes. No new dependencies/migrations.

## Remaining Work

Login/invitation request rate limiting requires a shared state strategy across
workers and verification of actual Cloudflare protections. LocMemCache alone
must not be treated as a shared rate limiter. Signup password policy, duplicate
username races and account lifecycle controls remain separate audit items.

The existing excluded-word preference uses GET to update state; only its write
fields were narrowed here. Converting state changes to POST/CSRF remains open.
An administrator deliberately changing quota is trusted and remains possible;
admin optimistic concurrency is not implemented here.

The patch prevents overspending current quota, but retries can legitimately
create another code when sufficient quota remains. Request idempotency and
abuse rate limiting are separate concerns, not guarantees of this patch.
