# Entry references

Developed on `codex/entry-references`; approved for the main release on 2026-09-27.

- `#123` links to an existing entry with an active author. Unknown IDs stay
  plain text; named hashtags retain their previous behavior. Numeric tokens
  no longer create new hashtag records. Existing records are not bulk deleted.
- `/entry/123/` redirects to the current single-entry page, so a title/slug
  change does not invalidate the copied short address.
- Entry menus copy either the reference or its short URL. The shared renderer
  handles previews and published content; Word/PDF retain clickable references.
- Code, formulas, escaped numbers, attributes and existing link labels are
  excluded. Rendering never generates notifications.

## Notifications

- Saving a published Answer sends `entry_reference` notifications for newly
  introduced, valid references to other authors. The same save groups multiple
  targets belonging to one author into one message.
- Existing references are compared with the persisted text before saving.
  Unrelated edits, partial saves of other fields, fixtures, drafts and previews
  do not send reference notifications. Accepting a proposed edit does send them
  when the new content is published.
- `EntryReferenceNotice` stores delivery history per source/target pair, with a
  database uniqueness constraint. Removing/re-adding a reference or deleting
  the notification does not permit repeat delivery. A new target in a later
  edit may produce a new notification, even when it has the same author.
- Notification creation and delivery history share a database transaction.
  Normal application publishing uses Answer.save(); bulk_create/QuerySet.update
  intentionally bypass signals and do not notify.
- Existing entries are not backfilled. Notifications link to the source entry
  through its short URL. The notification list has an Entry Referanslari filter.
- Navbar badges render unread counts on the initial response and refresh every
  15 seconds on visible pages, also on focus/visibility changes. This is polling,
  not a push channel. Cached navbar responses do not cache notification counts.
- Visiting the list does not mark notifications read. Opening an unread target
  with an ordinary click marks that notification read through a CSRF-protected
  POST; explicit individual/all-read controls remain available.

## Validation (2026-09-27)

- 38 focused Django tests passed (20 reference/export + 18 notification tests).
- Full suite after badge fixes: 735 tests, 730 passed, 5 existing SQLite row-lock tests skipped.
  MySQL parallel execution was not exercised by this local suite.
- Chrome with two temporary local accounts: log in, publish a reference through
  the form, receive the notification, open source entry, follow target reference,
  and copy the reference from the mobile menu. Passed; QA data was removed.
- Migration consistency and Django system checks passed.
- Badge regression coverage: 7 Django tests and 6 JavaScript tests passed.
  Local browser verification: initial count 1, automatic update to 2 without a
  reload, list visit preserves unread state, individual read reduces count to 1,
  and mark-all hides the badge. Temporary QA account/data removed afterward.

Migration `0064_entry_reference_notifications` is additive and was applied to
the local preview database. Deployment requires `python manage.py migrate`,
`collectstatic --noinput` and Web Reload after the eventual main merge/push.
