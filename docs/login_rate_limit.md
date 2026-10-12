# Login rate limiting

Date: 2026-10-07. Branch: codex/oturum-guvenligi-guncel, based on main b30a8ae.
Status: locally tested; NOT merged, pushed, configured or deployed in production.
This builds on the pending session-security patch in auth_session_security.md.

## Scope and behavior

- Public login and the configured Django admin login share the same budgets.
  Middleware resolves view names, not a hardcoded admin URL. It runs after CSRF
  validation and before credential validation/password hashing.
- A client network gets 60 attempts per 300 seconds; one normalized username
  from that network gets 10. Both successful and failed attempts count. Changing
  cookies, username casing or the server worker does not reset these counters.
- IPv4 uses one address, IPv4-mapped IPv6 is canonicalized to IPv4, native IPv6
  groups by /64 to limit address rotation. NFKC, trim and casefold normalize the
  username. MySQL collation aliases beyond this normalization are still bounded
  by the shared network budget.
- There is no global account lock. An attacker on another network cannot lock
  out the owner everywhere. People sharing one NAT or IPv6 /64 share the network
  budget; this is an explicit tradeoff, not perfect client identification.
- The window starts at the first attempt. Denied requests do not extend it.
  The response is HTTP 429 with Retry-After, no-store and a Turkish wait page.
  Existing sessions, reading pages, logout and GET login are not throttled.
- Unknown accounts receive the same limiting behavior. Passwords and raw
  usernames/IPs are never stored in the counter table. Keys are scope-separated
  HMAC-SHA256 digests using SECRET_KEY. Key rotation resets the effective budgets.
- Counter/IP-resolution errors return a generic 503 with Retry-After: they never
  silently disable protection. Error logs contain no submitted fields or headers.

## Shared database, expiry and concurrency

Migration 0065 adds LoginRateLimitBucket (digest primary key, attempts, indexed
expiry). No new production package, Redis service or LocMemCache is required.
The IP bucket is charged first so changing usernames cannot create unbounded
account buckets from one network during a window.

Creation commits before the row-lock transaction. This avoids a MySQL duplicate
insert/shared-lock deadlock reproduced in the first concurrency test. The short
transaction locks the bucket, checks expiry/limit, then increments. Password
hashing happens outside the transaction. A cleanup race retries up to 3 times;
continued failure rejects the attempt. This uses Django's normal read-committed
MySQL configuration; the current app does not use ATOMIC_REQUESTS.

Expired records can be reused, but cold records require maintenance. Run daily
in the production Web virtualenv after deployment:

```sh
cd /home/uia1/hafifAyaklar
/home/uia1/.virtualenvs/hafifAyaklar/bin/python manage.py cleanup_login_rate_limits
```

The command deletes only expired counters in batches of 500 and rechecks expiry
when deleting. It does not delete accounts, active budgets or sessions. No
scheduled task was created during this implementation. Review table growth and
install the cleanup task with the deployment; expiry alone does not delete rows.

## Proxy trust and rollout gate

Do not deploy until the actual request path is confirmed. The user has been
asked whether Cloudflare DNS proxying is enabled; the answer is still pending.

- Local/direct traffic: LOGIN_CLIENT_IP_SOURCE=remote_addr (local default).
  All arbitrary forwarded headers are ignored.
- PythonAnywhere: LOGIN_CLIENT_IP_SOURCE=pythonanywhere (hosted default).
  Only its overwritten X-Real-IP identifies the load balancer's upstream peer.
  Missing/invalid values fail closed, not back to the shared load balancer IP.
- Cloudflare in front of PythonAnywhere: additionally set
  LOGIN_TRUST_CLOUDFLARE=True ONLY after verifying that configuration.
  CF-Connecting-IP is trusted only if the PythonAnywhere-reported upstream peer
  belongs to the bundled official Cloudflare ranges. Direct-origin requests with
  spoofed CF headers use their own peer address. X-Forwarded-For is never used.
- A recognized Cloudflare edge without configured trust is rejected with 503,
  not counted as a shared client. This prevents a silent shared-edge lockout,
  but would block login if deployed before configuration. Do not ship blindly.
- Cloudflare Workers, Pseudo IPv4 "Overwrite Headers", visitor-IP removal,
  stacked CDNs and other proxies need separate review before enabling trust.
  Bundled Cloudflare ranges were checked against official lists on 2026-10-07;
  they must be reviewed when Cloudflare changes them. No runtime network fetch.
- LOGIN_RATE_LIMIT_PROXY_VERIFIED=True acknowledges completed verification;
  it does NOT change enforcement or prove that headers are authentic. Without
  it, `check --deploy` reports core.W010 on the hosted environment.

After release approval: configure the verified proxy settings, take the normal
DB backup, pull, migrate, collectstatic, check/check --deploy, Web Reload. Then
confirm a normal public/admin login, failed login and logout with a test account;
check two separate client networks are not grouped. Do not run brute-force tests
against production. Rollback requires reverting the app release and reloading;
the additive counter table can remain. Do not use an unverified header workaround.

## Validation

- Focused SQLite: rate-limit and session-security regressions; concurrency
  requiring row locks is validated separately on MySQL, not claimed for SQLite.
- Final full SQLite suite: 772 discovered, 766 passed, 6 row-lock tests skipped,
  22.628 seconds. No test failures. Five skips predate this change.
- MySQL 8.0.46 disposable Docker database: 37 focused tests passed, zero skips,
  3.921 seconds. Eight independent connections race on absent/live/expired
  buckets; precisely 3 of 8 are allowed with a budget of 3. Cleanup race and
  malformed proxy behavior covered. Existing Question.slug W003 warning remains.
- MySQL client was test-only PyMySQL 1.2.3 (install_as_MySQLdb); local native
  mysqlclient could not compile because client libraries were absent. Production
  requirements and driver were not changed. Production driver validation remains
  part of rollout, not implied by this isolated server test.
- Full requirements rebuilt in /private/tmp/hafif-validation-20261007 because
  the earlier temporary environment had been cleaned. No global venv changes.
- Browser against a synthetic SQLite DB: genuine CSRF form submission produced
  the 429 wait page; screenshot inspected; return to login works. No user data
  or production traffic was used. Temporary server/database/container removed.

## Remaining limits

This is not a DDoS shield, MFA or a global defense against distributed password
guessing. Many attacker networks can each consume their own budget. Edge rules,
account recovery/MFA and supported Django migration remain separate work.
Signup, exports and other expensive endpoints need their own policies. SEC-07
is not closed in production until proxy configuration and deployment are verified.

## Primary references

- https://help.pythonanywhere.com/pages/WebAppClientIPAddresses
- https://developers.cloudflare.com/fundamentals/reference/http-headers/
- https://www.cloudflare.com/ips-v4/
- https://www.cloudflare.com/ips-v6/
- https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
