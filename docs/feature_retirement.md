# Radio and Exit Test Retirement

Branch: codex/ozellik-kaldirma. Base: main 84b55ed.

## Scope

- Remove radio broadcasting/token/chat/count/DJ views, exit test views and
  forms, their templates, radio stylesheet and menu indicator code.
- Remove model admin registrations for the retired tools.
- Remove the global radio context processor: rendering ordinary pages no
  longer checks or updates broadcast state.
- Remove agora_token_builder from requirements. No dependency upgrade is
  included; already-installed packages need not be uninstalled during rollout.
- Old route prefixes return 410/noindex before the question slug catch-all.
  They cannot issue tokens, change counts or edit/delete old test records.
- Regular logout, logic lessons/exams, German lessons and polls are unaffected.

## Data and Attendance

Historical models and migrations are intentionally retained without public or
admin feature routes. No table, broadcast, chat message, exam or result is deleted.
Deleting this data later requires a separate explicit decision.

Attendance previously used UserProfile.is_dj. The Python field is now
can_manage_attendance (admin label: Devam Cetveli Yetkisi), mapped to the SAME
is_dj database column. Migration 0063 changes Django state only, performs no DDL
or data updates, and keeps existing access and old-code rollback compatibility.
Existing staff access remains; ordinary members do not gain permission.

## Verification and Rollout

Release check 2026-09-11: 602 tests passed on Django 4.2.2 (13.012 seconds). System checks,
makemigrations --check --dry-run and git diff --check passed. sqlmigrate 0063
reports no-op. No production database or live browser session was tested.
Prepared for main publication; production pull and Reload require user confirmation.

Run the complete Django suite, check, makemigrations --check --dry-run and
git diff --check. Dedicated tests cover old routes (GET/POST/DELETE), unregistered
admin models, preserved records, inherited attendance access, and absence of
radio queries during homepage rendering. Test database is isolated SQLite;
this is not a production/MySQL or browser end-to-end test.

After a future approved push: pull, activate the actual Web virtualenv, run
manage.py migrate (state-only 0063), collectstatic --noinput, check, then Web Reload.
The pending security package and .env removal are NOT part of this branch.

Agora account/project shutdown is external to the repository. Removing site
endpoints prevents new tokens from this code but does not revoke issued tokens
or close sessions already using the service. Disable unused Agora credentials
in its control panel separately; never paste their values into a report.

When merging the earlier security branch, DROP its radio view/template changes
and radio-specific tests instead of resurrecting retired files. Adapt any
attendance test fixtures to can_manage_attendance.
