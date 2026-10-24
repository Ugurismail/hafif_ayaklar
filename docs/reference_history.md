# Private Source Usage History

## Scope

- Clicking the source picker's insert button records a private usage event before
  inserting the citation into the editor. Saving a draft or publishing is not
  required. Merely creating a bibliography entry does not count as using it.
- Profile > Kaynaklarim > Kullanim gecmisim and the source modal's history icon
  open `/kaynak-gecmisim/`. Search, date/status filters and CSV export are available.
- UTC server time is authoritative; the UI and CSV display the configured local
  timezone (CSV includes its offset). This is an application timestamp, not a
  legally trusted timestamp or proof of authorship.
- Each deliberate insertion is a separate occurrence. Network retries reuse the
  event UUID. Account/event uniqueness prevents duplicate retry records.
- Saving a draft, reopening it, publishing it and editing the resulting entry
  retain the original creation time. Published entry links are shown in history.
- Bibliography and page snapshots survive source, draft and entry deletion;
  deleting the owner removes their history. Other users cannot query these rows.
  Public source usage statistics continue to use published entries only.

## Boundaries

- No historical timestamps are invented or backfilled. Existing citations and
  manually typed/pasted citation tokens do not produce insertion events.
- Discarding unsaved text does not discard its private history. Such records stay
  in the writing state. Removed citations are marked when the content is saved,
  not on every keystroke. Identical occurrences are reconciled by count, oldest
  first; the text syntax has no per-occurrence identity.
- A network failure leaves the editor unchanged and offers a retry. If the server
  recorded an event but its response was lost, the event can exist before the
  client inserts the token; retrying the same selection reuses that event.
- History has no separate delete UI in this version; it is intentionally retained
  when the associated draft/source is removed. It is private application data,
  not an immutable audit ledger.

## Safety and Cost

- Authenticated owner-only queries, POST + CSRF for recording, no-store responses.
- Payload/type/length validation, no HTML rendering of bibliography text, CSV
  formula escaping. No fetching external URLs or background workers.
- 300 insertions/account/hour; user row lock serializes limit/idempotency checks
  on MySQL. UUID uniqueness also enforces idempotency at database level.
- Indexed account/time history, 30-row pagination, streaming CSV. Only one small
  request per insertion; no polling or keystroke logging.
- Browser disables writing-form buttons/submission until the recording request
  finishes, restoring prior control states on both success and failure.

## Deployment

Migration `0069_reference_usage_history` creates a new table only. No dependency
change. Run migrate before Web Reload; collectstatic includes the new JS/CSS.

```bash
cd ~/hafifAyaklar
source /home/uia1/.virtualenvs/hafifAyaklar/bin/activate
git pull --ff-only origin main
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check
```

Then PythonAnywhere Web > Reload. Verify insertion before saving, private history,
draft/publish association and CSV in the deployed MySQL environment. Local tests
use SQLite and do not validate MySQL row-lock behavior.
