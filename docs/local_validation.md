# Isolated local validation

## 2026-09-26: test environment recovery

The old environment at `../venv` stalled during the general test run while
importing `reportlab.graphics.svgpath` and later while inspecting package
metadata with `pip check`. A separate, bounded SvgPath import subsequently
succeeded. `ls -lO` showed `compressed,dataless` on the old environment's
`reportlab/graphics/shapes.py`: its contents were not locally resident.

This is evidence of a local environment/file-availability problem, not proof
of a deterministic application deadlock. Do not remove diagram export tests,
mock the renderer, extend production timeouts, or alter application behavior
to bypass this failure.

A fresh venv was installed outside the Desktop/cloud-managed directory using
the existing requirements.txt. No existing venv, production settings, local
application database, or package pins were changed.

## Reproduce safely

Run from the project worktree. Use a separate local Python environment and an
explicit disposable SQLite database, never a production DATABASE_URL. The
temporary environment may be cleaned up by the OS; recreate it when absent.
Do not reuse a partially present temporary dependency directory via PYTHONPATH.

```sh
python3.11 -m venv /private/tmp/hafif-validation-20260926
/private/tmp/hafif-validation-20260926/bin/python -m pip install -r requirements.txt
/private/tmp/hafif-validation-20260926/bin/python -m pip check

export DATABASE_URL=sqlite:////private/tmp/hafif-validation-test.sqlite3
export DJANGO_SECRET_KEY=test-only-security-key-0123456789-abcdefghijklmnopqrstuvwxyz
export XDG_CACHE_HOME=/private/tmp/hafif-font-cache
# Apple Silicon macOS with Homebrew Pango already installed:
export DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib

/private/tmp/hafif-validation-20260926/bin/python -m weasyprint --info
/private/tmp/hafif-validation-20260926/bin/python manage.py test core.test_diagram_export core.test_paper_pdf --noinput --verbosity=2
/private/tmp/hafif-validation-20260926/bin/python manage.py test --noinput --verbosity=2
/private/tmp/hafif-validation-20260926/bin/python manage.py check
/private/tmp/hafif-validation-20260926/bin/python manage.py makemigrations --check --dry-run
node --test tests/js/entry_download.test.cjs
```

The explicit key above is disposable test configuration, never a production
secret. Django tests created their own in-memory test database. No application
database migrations were applied by this procedure. These are local validation
commands, not PythonAnywhere deployment commands.

For this investigation test commands ran through `subprocess.run(...,
timeout=180)` to bound a repeat of the stall. The complete verbose log was
written to `/private/tmp/hafif-validation-full-20260926.log`.

## Verified result

- Python 3.11.9, Django 4.2.2, ReportLab 4.4.4, resvg-py 0.5.0,
  WeasyPrint 70.0, Pydyf 0.12.1, native Pango 1.58.2 on macOS arm64.
- `pip check`: no broken requirements.
- Diagram and Word/PDF tests: 17 passed in 3.516 seconds. Tests rendered real
  diagrams/documents and checked nonblank images, Turkish text, links,
  footnotes, bibliography, permissions, and bounded timeout behavior.
- General suite: 690 discovered, 685 passed, 5 skipped, zero failures/errors;
  17.992 seconds. No tests were removed or bypassed for this result.
- Entry-download JavaScript: 8 passed.
- Migration drift check: no changes detected.

The five skips require row locking (`has_select_for_update`), unavailable in
SQLite: two parallel-voting tests and three invitation/quota/registration race
tests. They still need a dedicated MySQL/PostgreSQL test database. Never run
concurrency tests against the live PythonAnywhere database.

This resolves the local general-test execution blocker. It does not establish
production MySQL concurrency behavior, Google's indexing decisions, or
deployment completion. No main merge or push was performed.
