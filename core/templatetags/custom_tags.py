import re
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import escape
from core.models import Question, PollVote, Definition,Reference
from django.contrib.auth.models import User
from urllib.parse import quote_plus



register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 0)

@register.filter
def dict_get(dictionary, key):
    if dictionary is None:
        return None
    return dictionary.get(key)

@register.filter
def bkz_link(text):
    pattern = r'\(bkz:\s*(.*?)\)'
    def replace(match):
        query = match.group(1).strip()
        url = reverse('bkz', args=[query])
        return f'(bkz: <a href="{url}" target="_blank" rel="noopener noreferrer" style="text-decoration: none;">{escape(query)}</a>)'

    return mark_safe(re.sub(pattern, replace, text))


@register.filter
def ref_link(text):
    pattern = r'\((?:ref|r):([^\)]+)\)'
    def replace_ref(match):
        ref_text = match.group(1).strip()
        try:
            q = Question.objects.get(question_text__iexact=ref_text)
            url = reverse('question_detail', args=[q.slug])
            return f'<a href="{url}" target="_blank" style="text-decoration: none;">{escape(ref_text)}</a>'
        except Question.DoesNotExist:
            create_url = reverse('add_question_from_search') + f'?q={quote_plus(ref_text)}'
            return f'<a href="{create_url}" target="_blank" style="text-decoration: none;">{escape(ref_text)}</a>'

    # Sonucu mark_safe() ile işaretleyerek HTML'nin render edilmesini sağlıyoruz.
    return mark_safe(re.sub(pattern, replace_ref, text))

@register.filter
def user_has_voted(options, user):
    return PollVote.objects.filter(option__in=options, user=user).exists()

@register.filter
def field_by_name(form, name):
    return form[name]

@register.filter
def split(value, separator=' '):
    return value.split(separator)

@register.filter
def tanim_link(text):
    """
    Metin içerisinde (tanim:Özgürlük:42) kalıplarını yakalayıp, popover oluşturur.
    """
    if not text:
        return ""

    # Pattern: (tanim:kelime:ID) veya kısa form (t:kelime:ID)
    #  Grup 1 => kelime
    #  Grup 2 => id
    pattern = re.compile(r'\((?:tanim|t):([^:]+):(\d+)\)')

    def replacer(match):
        question_word = match.group(1).strip()  # "Özgürlük"
        def_id_str    = match.group(2).strip()  # "42"
       

        try:
            definition = Definition.objects.get(id=def_id_str)
            # Tanım metni
            def_text   = definition.definition_text
            # (İstersen "definition.user.username" vs. de popover’a ekleyebilirsin.)
            user_name = definition.user.username


            # HTML popover
            # Bootstrap 5: data-bs-toggle="popover" data-bs-content="..."
            # Hover/focus ile açtırmak için -> data-bs-trigger="hover focus"
            return f'''<span class="tanim-popover" 
                          style="text-decoration:underline; cursor:pointer;"
                          data-bs-toggle="popover" 
                          data-bs-placement="top" 
                          data-bs-trigger="hover focus"
                          data-bs-title="{escape(user_name)}"
                          data-bs-content="{escape(def_text)}">
                          {escape(question_word)}
                       </span>'''
        except Definition.DoesNotExist:
            # ID bulunamadıysa => orijinal metni döndürmek yerine 
            # plain text olarak "kelime" döndürebiliriz veya "Tanım yok" diyen bir span.
            return escape(question_word)

    # text içinde tüm (tanim:word:id) kalıplarını replacer ile değiştir.
    new_text = pattern.sub(replacer, text)

    return mark_safe(new_text)

@register.filter
def reference_link(text):
    """
    Metin içinde (kaynak:ID[, sayfa:NUM]) kalıplarını yakalar.
    Her unique ID için sırayla [1], [2], [3] vs. gösterir.
    Hover (veya tooltip) ile tam künyeyi gösterir.
    """
    if not text:
        return ""

    reference_map = {}
    current_index = 1

    pattern = re.compile(r'\((?:kaynak|k):(\d+)(?:(?:,\s*sayfa:([^)]+))|(?:\s*s:([^)]+)))?\)')

    def replace_reference(match):
        nonlocal current_index
        ref_id_str = match.group(1)
        sayfa = match.group(2) or match.group(3)  # Opsiyonel: None veya string (12-14, 123a vs.)
        ref_id = int(ref_id_str)

        if ref_id not in reference_map:
            reference_map[ref_id] = current_index
            current_index += 1

        ref_num = reference_map[ref_id]

        try:
            ref_obj = Reference.objects.get(id=ref_id)

            # Çoklu yazarları düzgün formatla
            surnames = [s.strip() for s in ref_obj.author_surname.split(';') if s.strip()]
            names = [n.strip() for n in ref_obj.author_name.split(';') if n.strip()]

            authors = []
            for i in range(max(len(surnames), len(names))):
                surname = surnames[i] if i < len(surnames) else ''
                name = names[i] if i < len(names) else ''
                if surname or name:
                    authors.append(f"{surname}, {name}".strip(', '))

            author_str = '; '.join(authors)
            metin = f". {ref_obj.metin_ismi}" if ref_obj.metin_ismi else ""
            full_citation = f"{author_str}{metin} ({ref_obj.year}). {ref_obj.rest}"
            if ref_obj.abbreviation:
                full_citation += f" [{ref_obj.abbreviation}]"
            if sayfa:
                full_citation += f", s. {sayfa.strip()}"
        except Reference.DoesNotExist:
            full_citation = f"Kaynak bulunamadı (ID: {ref_id})"

        html = f'<sup class="reference-tooltip" data-bs-toggle="tooltip" title="{escape(full_citation)}">[{ref_num}]</sup>'
        return html

    new_text = pattern.sub(replace_reference, text)
    return mark_safe(new_text)

@register.filter
def highlight(text, keyword):
    """
    'text' içinde 'keyword' kelimesi geçiyorsa, 
    <mark>...</mark> ile vurgulansın (case-insensitive).
    """
    if not keyword:
        return text  # aranan kelime boşsa, değiştirmeden dön

    # Tüm 'keyword' geçen yerleri bul, <mark> ekle
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    highlighted = pattern.sub(
        lambda m: f'<mark>{m.group(0)}</mark>',
        text
    )
    return mark_safe(highlighted)

@register.filter
def mention_link(text):
    # @ ile başlayan ve sonrasında max 3 kelime yakala
    # Use `\w` to support unicode letters like î/û/â etc, and normalize common dash variants.
    pattern = r'@([\w.\-\u00A0 ]{1,50})'  # 50 karakterlik kullanıcı adı limiti

    def replace(match):
        import unicodedata

        candidate = unicodedata.normalize('NFKC', match.group(1))
        candidate = candidate.replace('\u00A0', ' ')  # nbsp -> space
        for dash in ('‐', '‑', '‒', '–', '—', '−'):
            candidate = candidate.replace(dash, '-')
        candidate = ' '.join(candidate.split())

        words = candidate.split()
        for i in range(len(words), 0, -1):
            username = ' '.join(words[:i])
            try:
                user = User.objects.get(username__iexact=username)
                url = reverse('user_profile', args=[user.username])
                # kalan kelimeler ek veya düz metin olur
                tail = ' '.join(words[i:])
                safe_username = escape(username)
                safe_tail = escape(tail) if tail else ""
                return f'<a href="{url}" class="mention">@{safe_username}</a>{(" " + safe_tail) if safe_tail else ""}'
            except User.DoesNotExist:
                continue
        # hiçbiri yoksa düz metin döndür
        return f'@{escape(candidate)}'

    result = re.sub(pattern, replace, text)
    return mark_safe(result)

@register.filter
def hashtag_link(text):
    """
    Convert #hashtags to clickable links
    Supports Turkish characters: ç, ğ, ı, ö, ş, ü and their uppercase versions
    """
    # Hashtag pattern with explicit Turkish character support
    pattern = r'(?:^|[^A-Za-z0-9_ğüşöçıİĞÜŞÖÇ])(#([A-Za-z0-9_ğüşöçıİĞÜŞÖÇ]+))'

    def replace(match):
        prefix = match.group(0)[0] if len(match.group(0)) > 1 and match.group(0)[0] != '#' else ''
        hashtag_name = match.group(2)
        url = reverse('hashtag_view', args=[hashtag_name.lower()])
        return f'{prefix}<a href="{url}" class="hashtag-link">#{hashtag_name}</a>'

    result = re.sub(pattern, replace, text)
    return mark_safe(result)

@register.filter
def safe_markdownify(text, arg='default'):
    """
    Markdownify with hashtag protection
    Converts hashtags to placeholders before markdown, then restores them
    Supports Turkish characters: ç, ğ, ı, ö, ş, ü and their uppercase versions
    """
    import uuid
    from markdownify.templatetags.markdownify import markdownify as original_markdownify

    if not text:
        return ""

    # Store hashtags with unique placeholders
    hashtag_map = {}
    # Pattern with explicit Turkish character support
    pattern = r'(?:^|[^A-Za-z0-9_ğüşöçıİĞÜŞÖÇ])(#([A-Za-z0-9_ğüşöçıİĞÜŞÖÇ]+))'

    def replace_with_placeholder(match):
        hashtag_name = match.group(2)
        placeholder = f"HASHTAG_{uuid.uuid4().hex[:8]}_{hashtag_name}"
        url = reverse('hashtag_view', args=[hashtag_name.lower()])
        hashtag_map[placeholder] = f'<a href="{url}" class="hashtag-link">#{hashtag_name}</a>'
        # Return placeholder with prefix to prevent markdown interpretation
        prefix = match.group(0)[0] if len(match.group(0)) > 1 and match.group(0)[0] != '#' else ''
        return f'{prefix}{placeholder}'

    # Replace hashtags with placeholders
    text_with_placeholders = re.sub(pattern, replace_with_placeholder, text)

    # Protect TeX blocks so Markdown doesn't eat backslashes like `\\` (align/matrix).
    # We restore as HTML-escaped text so BLEACH safety is preserved.
    math_map = {}
    display_math_re = re.compile(r'\$\$(.+?)\$\$', re.DOTALL)
    inline_math_re = re.compile(r'(?<!\\)\$(?!\$)(.+?)(?<!\\)\$(?!\$)', re.DOTALL)

    def _normalize_math_backslashes(raw_block: str) -> str:
        """
        Normalize double-escaped TeX commands inside math blocks.
        Example: $$\\int_0^\\infty$$ -> $$\\int_0^\\infty$$ with single slashes.
        """
        if raw_block.startswith('$$') and raw_block.endswith('$$'):
            delim = '$$'
            content = raw_block[2:-2]
        elif raw_block.startswith('$') and raw_block.endswith('$'):
            delim = '$'
            content = raw_block[1:-1]
        else:
            delim = ''
            content = raw_block

        # Convert accidental double-escaped commands (\\int -> \int) without touching line breaks.
        content = re.sub(r'\\\\([A-Za-z])', r'\\\1', content)
        # Fix accidental single backslash row breaks like "\3" or "\ 3" -> "\\ 3".
        content = re.sub(r'\\\s*(\d)', lambda m: "\\\\ " + m.group(1), content)
        return f"{delim}{content}{delim}"

    def _store_math_block(raw_block: str) -> str:
        # Some users naturally end TeX lines with a single "\" before newline.
        # In TeX environments like align/pmatrix, line breaks require "\\".
        # Normalize only the "backslash + newline" case to avoid touching valid commands.
        raw_block = re.sub(r'\\[ \t]*\r?\n', r'\\\\\n', raw_block)
        raw_block = _normalize_math_backslashes(raw_block)
        placeholder = f"MATH_{uuid.uuid4().hex[:10]}_END"
        math_map[placeholder] = escape(raw_block)
        return placeholder

    def _replace_display(match):
        raw = match.group(0)
        return _store_math_block(raw)

    def _replace_inline(match):
        raw = match.group(0)
        return _store_math_block(raw)

    text_with_placeholders = display_math_re.sub(_replace_display, text_with_placeholders)
    text_with_placeholders = inline_math_re.sub(_replace_inline, text_with_placeholders)

    # Apply markdown
    markdown_result = original_markdownify(text_with_placeholders, arg)

    # Add target="_blank" to all external links (not hashtag links)
    # This makes all markdown links open in new tab
    markdown_result = re.sub(
        r'<a\s+href="([^"]+)"',
        r'<a href="\1" target="_blank" rel="noopener noreferrer"',
        markdown_result
    )

    # Restore hashtags (these will override the target="_blank" for internal links)
    for placeholder, hashtag_html in hashtag_map.items():
        markdown_result = markdown_result.replace(placeholder, hashtag_html)

    # Restore math blocks last (still HTML-escaped so it stays safe).
    for placeholder, math_html in math_map.items():
        markdown_result = markdown_result.replace(placeholder, math_html)

    return mark_safe(markdown_result)

@register.filter
def truncate_math_safe(text, length=1000):
    """
    Truncate text without cutting inside TeX math blocks ($...$ / $$...$$).
    This prevents partial math (e.g. an opening $$ without closing $$) from
    appearing on summary cards (user_homepage, question_detail, etc.).
    """
    if not text:
        return ""

    try:
        max_len = int(length)
    except (TypeError, ValueError):
        return text

    if max_len <= 0 or len(text) <= max_len:
        return text

    in_display = False
    in_inline = False
    last_safe = 0
    i = 0

    limit = min(max_len, len(text))
    while i < limit:
        ch = text[i]

        # Skip escaped characters (e.g. \$)
        if ch == '\\':
            i += 2
            continue

        if ch == '$':
            # Toggle display math with $$
            if i + 1 < len(text) and text[i + 1] == '$':
                in_display = not in_display
                i += 2
                continue

            # Toggle inline math with $
            in_inline = not in_inline
            i += 1
            continue

        if not in_display and not in_inline:
            last_safe = i + 1

        i += 1

    cut_at = last_safe if last_safe > 0 else max_len
    return text[:cut_at]

@register.filter
def extract_bibliography(text):
    """
    Extract unique references from text and return them as a list of dicts.
    Each dict contains {'number': int, 'reference': Reference, 'pages': list}.
    This maintains the same numbering order as reference_link filter.
    Returns a list suitable for rendering the bibliography section.
    """
    if not text:
        return []

    reference_map = {}
    reference_pages = {}  # Store page numbers for each reference
    current_index = 1

    pattern = re.compile(r'\((?:kaynak|k):(\d+)(?:(?:,\s*sayfa:([^)]+))|(?:\s*s:([^)]+)))?\)')
    matches = pattern.finditer(text)

    for match in matches:
        ref_id_str = match.group(1)
        sayfa = match.group(2) or match.group(3)  # Optional: None or string (12-14, 123a etc.)
        ref_id = int(ref_id_str)

        if ref_id not in reference_map:
            reference_map[ref_id] = current_index
            reference_pages[ref_id] = []
            current_index += 1

        # Collect page numbers if they exist
        if sayfa:
            page_str = sayfa.strip()
            if page_str not in reference_pages[ref_id]:
                reference_pages[ref_id].append(page_str)

    # Build the bibliography list
    bibliography = []
    for ref_id, ref_num in sorted(reference_map.items(), key=lambda x: x[1]):
        try:
            ref_obj = Reference.objects.get(id=ref_id)
            pages = reference_pages.get(ref_id, [])

            # Çoklu yazarları düzgün formatla
            surnames = [s.strip() for s in ref_obj.author_surname.split(';') if s.strip()]
            names = [n.strip() for n in ref_obj.author_name.split(';') if n.strip()]

            authors = []
            for i in range(max(len(surnames), len(names))):
                surname = surnames[i] if i < len(surnames) else ''
                name = names[i] if i < len(names) else ''
                if surname or name:
                    authors.append(f"{surname}, {name}".strip(', '))

            formatted_authors = '; '.join(authors)

            bibliography.append({
                'number': ref_num,
                'reference': ref_obj,
                'formatted_authors': formatted_authors,
                'pages': pages
            })
        except Reference.DoesNotExist:
            bibliography.append({
                'number': ref_num,
                'reference': None,
                'ref_id': ref_id,
                'pages': []
            })

    return bibliography

@register.filter
def spoiler_link(text):
    """
    -g- text -g- veya --gizli--text--gizli-- formatını * işaretine çevirir, hover'da içeriği gösterir
    """
    def replace(match):
        hidden_text = match.group(1).strip()
        # HTML encode to prevent XSS
        from html import escape
        escaped_text = escape(hidden_text)
        return f'<span class="spoiler-text" data-bs-toggle="tooltip" data-bs-html="true" title="{escaped_text}">*</span>'

    # Yeni kısa format: -g- text -g-
    pattern_new = r'-g-\s+(.*?)\s+-g-'
    text = re.sub(pattern_new, replace, text, flags=re.DOTALL)

    # Eski format için backward compatibility: --gizli--text--gizli--
    pattern_old = r'--gizli--(.*?)--gizli--'
    text = re.sub(pattern_old, replace, text, flags=re.DOTALL)

    return mark_safe(text)
