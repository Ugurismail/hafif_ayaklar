# Content and Paper Export Improvements

Date: 2026-09-12. Branch: codex/icerik-iyilestirmeleri.
Base: origin/main 93841c7. Local only; not pushed or deployed.

## Delivered Scope

- Word now uses the existing paper DOCX layout. The separate Paper option was
  removed from the download interface; its endpoint remains a compatibility
  alias. PDF projects the same generated DOCX into a constrained print layout,
  including headings, internal contents links, footnotes, bibliography,
  numbered outlines, pictures and diagrams. Word keeps Garamond; PDF embeds
  the bundled OFL-licensed EB Garamond, so pagination need not be identical.
- PDF resource fetching accepts only generated images and fixed bundled fonts,
  not arbitrary network or local-file URLs. Its separate worker has a 60-second
  timeout and Linux CPU/address-space limits. Missing footnote text fails the
  export rather than silently delivering an incomplete document. These limits
  do not replace a future total-book budget or background export queue.
- Numbered outlines no longer stop after four levels in entry display or Word
  paper export. Semantic levels remain intact; visual indentation is capped
  to keep deep content within the page. Tests cover 24 levels.
- Invitation codes have compact, aligned, accessible copy buttons, success
  feedback and readable table headers. The mobile table scrolls horizontally;
  codes wrap to two lines with their copy button visible before scrolling.
  Clipboard failure is reported without modifying any invitation data.
- Paper DOCX export embeds diagrams, fitting actual paths, curves, shapes and
  freehand strokes rather than the editor's empty canvas. The image is bounded
  to 2200 pixels before final whitespace cropping and padding.
- Described arrows receive numbered markers and corresponding explanation
  text below the image. Opposite-direction connections retain their separate
  annotation positions. Node links and long node text are also included below
  the diagram. References in arrow descriptions participate in paper notes
  and the bibliography. Existing text before/after an inline diagram survives.
- Export uses the existing normalized diagram model and server geometry, not
  arbitrary submitted SVG. SVG elements are allowlisted, active attributes
  removed, and only bundled fonts and a fixed print stylesheet are used.
  Linked node URLs are text, never fetched as rendering resources.

## Verification

- Full isolated SQLite suite with a fresh requirements install: 643 discovered,
  641 passed, 2 skipped, 18.737s.
- All 25 interaction-security tests passed on isolated MySQL 8.0.46, including
  the two parallel-vote tests skipped by SQLite. See content_security.md.
- Chrome/Playwright at 1440px and 390px: actual clipboard contents match the
  selected code; outlines do not horizontally overflow; mobile table rows
  remain compact and copy buttons are visible; header colors are readable.
- A generated DOCX was rendered through LibreOffice to PDF and both pages
  visually inspected. The figure, numbered descriptions, node URL and 14-level
  outline remain readable. This is a sample, not exhaustive visual coverage
  of every user-authored shape combination or arbitrary document size.
- Export regressions cover invalid payloads, active-content exclusion,
  nonblank bounded raster output, large curves, freehand strokes, reverse
  connections, inline diagram placement and bibliography integration.
- Nine additional PDF/Word tests cover selection/order, access control,
  escaped content, blocked external resources, worker failure, diagrams,
  citations, page-local footnotes and symbol restart on successive pages.
  All six pages of two final PDF samples were visually reviewed, including
  the diagram, 14-level outline, bibliography and a long footnote.

## Deployment Notes

No model or migration changes in this patch. Export adds resvg-py==0.5.0,
weasyprint==70.0 and pypdf==6.8.0. tinycss2==1.5.1 and bleach==6.4.0 provide
compatible CSS dependencies. Pango was installed and verified locally;
PythonAnywhere's native libraries have NOT yet been verified. After publication
is separately approved, install requirements in the PythonAnywhere WEB
virtualenv and run `python -m weasyprint --info` before Web Reload. Verify a
real PDF download after deployment. Collect static files and run Django checks.
Do not use the similarly
named old project-local virtualenv by accident. Do not publish this branch
without explicit approval.

The current preview uses an isolated copy of local data, not production.
The worktree is stored permanently under
`/Users/ugurismail/Desktop/hafif_ayaklar/icerik_iyilestirmeleri_worktree`.
Earlier uncommitted diagram-editor work in the parent checkout is preserved
and intentionally not mixed into this branch.

## Follow-Up Diagram Work

1. Review the separate editor changes against main before any merge; verify
   the same description/link indicators in editor, published entry and viewer.
2. Test complex intersections, independent arrows and long labels across
   saved documents, undo/redo and export, with representative real examples.
3. Add measured export-size/time budgets and background processing for large
   books. Per-diagram payload and image limits are not a total book limit.
4. Evaluate vector-preserving paper output and selectable labels separately;
   the current Word figure is raster, while explanations remain regular text.
5. Audit keyboard/touch access and explanatory labels in the editor without
   loading new editor code on ordinary pages that do not use diagrams.

Passing this patch's tests does not certify the entire site as secure or
prove production performance. Runtime upgrades and other audit items remain
tracked in content_security.md.

Dependency references: https://doc.courtbouillon.org/weasyprint/stable/api_reference.html,
https://github.com/google/fonts/tree/main/ofl/ebgaramond,
https://bleach.readthedocs.io/en/latest/changes.html.
