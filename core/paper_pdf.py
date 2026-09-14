"""PDF projection of our generated Word document, not a general DOCX converter."""

from html import escape
from io import BytesIO
from pathlib import Path
from urllib.parse import urlsplit
import re
import subprocess
import sys
import unicodedata
import zipfile

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from lxml import etree

ROOT = Path(__file__).resolve().parent.parent
ASSET_ROOT = 'https://paper.invalid/'
FONT_FILES = ('EBGaramond-Variable.ttf', 'EBGaramond-Italic-Variable.ttf', 'DejaVuSans.ttf')
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
MAX_DOCUMENT_BYTES = 32 * 1024 * 1024
PDF_TIMEOUT_SECONDS = 60


class PDFExportError(Exception):
    pass


def _safe_link(url):
    if not url or any(ord(c) < 32 for c in url):
        return None
    try:
        parsed = urlsplit(url)
    except ValueError:
        return None
    if parsed.scheme in {'http', 'https'} and parsed.netloc:
        return url
    if parsed.scheme == 'mailto' and parsed.path:
        return url
    return None


def _inherited(paragraph, owner, name):
    value = getattr(getattr(paragraph, owner), name) if owner == 'paragraph_format' else None
    if value is not None:
        return value
    style = paragraph.style
    while style is not None:
        value = getattr(getattr(style, owner), name)
        if value is not None:
            return value
        style = style.base_style
    return None


def _paragraph_css(paragraph):
    declarations = []
    for name, css_name in (
        ('left_indent', 'margin-left'), ('right_indent', 'margin-right'),
        ('first_line_indent', 'text-indent'), ('space_before', 'margin-top'),
        ('space_after', 'margin-bottom'),
    ):
        value = _inherited(paragraph, 'paragraph_format', name)
        if value is not None:
            declarations.append(f'{css_name}:{value.pt:g}pt')
    alignment = _inherited(paragraph, 'paragraph_format', 'alignment')
    alignments = {WD_ALIGN_PARAGRAPH.LEFT: 'left', WD_ALIGN_PARAGRAPH.CENTER: 'center',
                  WD_ALIGN_PARAGRAPH.RIGHT: 'right', WD_ALIGN_PARAGRAPH.JUSTIFY: 'justify'}
    if alignment in alignments:
        declarations.append(f'text-align:{alignments[alignment]}')
    spacing = _inherited(paragraph, 'paragraph_format', 'line_spacing')
    if spacing is not None:
        declarations.append(f'line-height:{spacing.pt:g}pt' if hasattr(spacing, 'pt') else f'line-height:{spacing:g}')
    for name, css_name in (('keep_with_next', 'break-after'), ('keep_together', 'break-inside')):
        if _inherited(paragraph, 'paragraph_format', name):
            declarations.append(f'{css_name}:avoid')
    if _inherited(paragraph, 'paragraph_format', 'page_break_before'):
        declarations.append('break-before:page')
    size = _inherited(paragraph, 'font', 'size')
    if size is not None:
        declarations.append(f'font-size:{size.pt:g}pt')
    if _inherited(paragraph, 'font', 'bold'):
        declarations.append('font-weight:bold')
    if _inherited(paragraph, 'font', 'italic'):
        declarations.append('font-style:italic')
    return ';'.join(declarations)


class _WordProjection:
    def __init__(self, document_bytes):
        self.document = Document(BytesIO(document_bytes))
        self.assets = {}
        self.notes = {}
        self.note_marks = {}
        self._paragraph_css_cache = {}
        with zipfile.ZipFile(BytesIO(document_bytes)) as archive:
            if 'word/footnotes.xml' in archive.namelist():
                root = etree.fromstring(archive.read('word/footnotes.xml'),
                                        etree.XMLParser(resolve_entities=False, no_network=True))
                for note in root.findall('w:footnote', NS):
                    if int(note.get(qn('w:id'))) > 0:
                        self.notes[note.get(qn('w:id'))] = ''.join(note.itertext()).strip()
        self.note_marks = {note_id: '*' for note_id in self.notes}

    def paragraph_css(self, paragraph):
        properties = paragraph._p.pPr
        key = (paragraph.style.style_id,
               etree.tostring(properties) if properties is not None else b'')
        if key not in self._paragraph_css_cache:
            self._paragraph_css_cache[key] = _paragraph_css(paragraph)
        return self._paragraph_css_cache[key]

    def fetch_asset(self, url, *args, **kwargs):
        # Never delegate to a network/file fetcher, including for nested SVG/CSS.
        if url not in self.assets:
            raise ValueError('PDF resource is not a generated document asset')
        data, mime_type = self.assets[url]
        return {'string': data, 'mime_type': mime_type}

    def _image(self, drawing):
        blips = drawing.xpath('.//a:blip')
        extents = drawing.xpath('.//wp:extent')
        if not blips or not extents:
            return ''
        relationship_id = blips[0].get(qn('r:embed'))
        part = self.document.part.related_parts.get(relationship_id)
        if part is None or part.content_type not in {'image/png', 'image/jpeg'}:
            return ''
        url = ASSET_ROOT + f'image-{relationship_id}'
        self.assets[url] = (part.blob, part.content_type)
        width = int(extents[0].get('cx')) / 12700
        height = int(extents[0].get('cy')) / 12700
        descriptions = drawing.xpath('.//wp:docPr')
        alt = descriptions[0].get('descr', '') if descriptions else ''
        return f'<img src="{url}" alt="{escape(alt, quote=True)}" style="width:{width:g}pt;height:{height:g}pt">'

    def _run(self, run):
        pieces = []
        for child in run:
            if child.tag == qn('w:t'):
                pieces.append(escape(child.text or ''))
            elif child.tag == qn('w:tab'):
                pieces.append('<span class="tab">&#160;</span>')
            elif child.tag == qn('w:br') and child.get(qn('w:type')) != 'page':
                pieces.append('<br>')
            elif child.tag == qn('w:drawing'):
                pieces.append(self._image(child))
            elif child.tag == qn('w:footnoteReference'):
                note_id = child.get(qn('w:id'))
                text = self.notes.get(note_id, '')
                mark = self.note_marks.get(note_id, '*')
                pieces.append(f'<span id="note-call-{note_id}"><span class="footnote" data-note-mark="{escape(mark, quote=True)}">{escape(text)}</span></span>')
        text = ''.join(pieces)
        properties = run.find(qn('w:rPr'))
        if properties is None:
            return text
        declarations = []
        for tag, css in (('b', 'font-weight:bold'), ('i', 'font-style:italic')):
            prop = properties.find(qn('w:' + tag))
            if prop is not None and prop.get(qn('w:val'), '1') not in {'0', 'false', 'off'}:
                declarations.append(css)
        size = properties.find(qn('w:sz'))
        if size is not None:
            declarations.append(f'font-size:{int(size.get(qn("w:val"))) / 2:g}pt')
        color = properties.find(qn('w:color'))
        if color is not None and re.fullmatch(r'[0-9a-fA-F]{6}', color.get(qn('w:val'), '')):
            declarations.append(f'color:#{color.get(qn("w:val"))}')
        return f'<span style="{";".join(declarations)}">{text}</span>' if declarations else text

    def _inline(self, paragraph):
        pieces = []
        for child in paragraph._p:
            if child.tag == qn('w:r'):
                pieces.append(self._run(child))
            elif child.tag == qn('w:hyperlink'):
                text = ''.join(self._run(run) for run in child.findall(qn('w:r')))
                anchor = child.get(qn('w:anchor'))
                if anchor and re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', anchor):
                    href = '#' + anchor
                else:
                    rel = self.document.part.rels.get(child.get(qn('r:id')))
                    href = _safe_link(rel.target_ref) if rel is not None and rel.is_external else None
                pieces.append(f'<a href="{escape(href, quote=True)}">{text}</a>' if href else text)
        return ''.join(pieces)

    def html(self):
        pieces = []
        for paragraph in self.document.paragraphs:
            if paragraph._p.xpath('.//w:br[@w:type="page"]'):
                pieces.append('<div class="page-break"></div>')
                continue
            if paragraph._p.xpath('./w:pPr/w:pBdr'):
                pieces.append('<hr>')
                continue
            content = self._inline(paragraph)
            if not content:
                continue
            name = paragraph.style.name
            heading = re.fullmatch(r'Heading ([1-9])', name)
            tag = f'h{min(int(heading.group(1)), 6)}' if heading else 'p'
            attributes = []
            if heading:
                attributes.append(f'role="heading" aria-level="{heading.group(1)}"')
            bookmarks = paragraph._p.findall(qn('w:bookmarkStart'))
            if bookmarks:
                attributes.append(f'id="{escape(bookmarks[0].get(qn("w:name")), quote=True)}"')
            class_name = {
                'Paper TOC Heading': 'toc-heading', 'Paper TOC Entry': 'toc-entry',
                'Paper Numbered Item': 'numbered', 'Paper Bibliography': 'bibliography',
                'Paper Quote': 'quote', 'Caption': 'caption',
            }.get(name, 'body')
            if name == 'Paper Numbered Item':
                # Word uses a hanging tab; keep marker/content in separate columns.
                marker, separator, remainder = content.partition('<span class="tab">&#160;</span>')
                if separator:
                    content = f'<span class="marker">{marker}</span><span>{remainder}</span>'
            css = self.paragraph_css(paragraph)
            if name == 'Paper Numbered Item':
                left = _inherited(paragraph, 'paragraph_format', 'left_indent')
                hanging = _inherited(paragraph, 'paragraph_format', 'first_line_indent')
                if left is not None and hanging is not None:
                    css += f';padding-left:{max(0, left.pt + hanging.pt):g}pt'
            pieces.append(f'<{tag} class="{class_name}" style="{css}" {" ".join(attributes)}>{content}</{tag}>')
        title = escape(self.document.core_properties.title or 'Entryler')
        author = escape(self.document.core_properties.author or '', quote=True)
        return f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>{title}</title><meta name="author" content="{author}"></head><body>{"".join(pieces)}</body></html>'


def _render_pdf(document_bytes):
    from weasyprint import CSS, HTML
    from weasyprint.urls import URLFetcher, URLFetcherResponse
    from weasyprint.text.fonts import FontConfiguration

    projection = _WordProjection(document_bytes)
    for filename in FONT_FILES:
        projection.assets[ASSET_ROOT + filename] = ((ROOT / 'static/fonts' / filename).read_bytes(), 'font/ttf')
    class DocumentAssets(URLFetcher):
        def fetch(self, url, headers=None):
            resource = projection.fetch_asset(url)
            return URLFetcherResponse(url, resource['string'], {'Content-Type': resource['mime_type']})

    fetcher = DocumentAssets(fail_on_errors=True)
    font_config = FontConfiguration()
    css = CSS(string=(ROOT / 'static/css/paper_pdf.css').read_text(encoding='utf-8'),
              url_fetcher=fetcher, font_config=font_config)
    for _ in range(5):
        document = HTML(string=projection.html(), url_fetcher=fetcher).render(
            stylesheets=[css], font_config=font_config,
        )
        marks = {}
        for page in document.pages:
            note_ids = sorted(int(name.removeprefix('note-call-')) for name in page.anchors if name.startswith('note-call-'))
            for index, note_id in enumerate(note_ids):
                marks[str(note_id)] = ('*', '†', '‡', '§', '‖', '¶')[index % 6] * (index // 6 + 1)
        if marks == projection.note_marks:
            pdf = document.write_pdf()
            _verify_note_text(pdf, projection.notes.values())
            return pdf
        projection.note_marks = marks
    raise PDFExportError('PDF dipnot yerleşimi tamamlanamadı. Word biçimini kullanabilirsiniz.')


def _verify_note_text(pdf, notes):
    if not notes:
        return
    from pypdf import PdfReader
    def normalize(text):
        return ''.join(unicodedata.normalize('NFKC', text).split())
    text = normalize('\n'.join(page.extract_text() for page in PdfReader(BytesIO(pdf)).pages))
    if any(normalize(note) not in text for note in notes):
        raise PDFExportError('Uzun dipnotlar PDF sayfasına yerleştirilemedi. Word biçimini kullanabilirsiniz.')


def paper_docx_to_pdf(document_bytes):
    if len(document_bytes) > MAX_DOCUMENT_BYTES:
        raise PDFExportError('PDF için daha az entry seçerek tekrar deneyin.')
    # Isolate native font/layout failures and stop pathological pagination.
    interpreter = Path(sys.prefix) / 'bin/python'
    try:
        result = subprocess.run(
            [str(interpreter) if interpreter.is_file() else sys.executable, '-m', 'core.paper_pdf'], cwd=ROOT,
            input=document_bytes, capture_output=True, timeout=PDF_TIMEOUT_SECONDS,
            check=True,
        )
    except subprocess.TimeoutExpired as exc:
        raise PDFExportError('PDF oluşturma süresi aşıldı. Daha az entry seçerek tekrar deneyin.') from exc
    except (subprocess.CalledProcessError, OSError) as exc:
        raise PDFExportError('PDF oluşturulamadı. Word biçimini kullanabilir veya daha sonra tekrar deneyebilirsiniz.') from exc
    if not result.stdout.startswith(b'%PDF-'):
        raise PDFExportError('PDF çıktısı doğrulanamadı. Word biçimini kullanabilirsiniz.')
    return result.stdout


if __name__ == '__main__':
    if sys.platform.startswith('linux'):
        import resource
        resource.setrlimit(resource.RLIMIT_AS, (1024 ** 3, 1024 ** 3))
        resource.setrlimit(resource.RLIMIT_CPU, (PDF_TIMEOUT_SECONDS, PDF_TIMEOUT_SECONDS))
    data = sys.stdin.buffer.read(MAX_DOCUMENT_BYTES + 1)
    if len(data) > MAX_DOCUMENT_BYTES:
        raise SystemExit('Document exceeds PDF size budget')
    sys.stdout.buffer.write(_render_pdf(data))
