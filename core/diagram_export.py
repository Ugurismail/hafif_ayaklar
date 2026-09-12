"""Static diagram rendering for documents; never accepts user-provided SVG."""

from pathlib import Path
from io import BytesIO
import re
from lxml import etree
from PIL import Image, ImageChops, ImageOps
from .diagram_markup import decode_diagram_payload, render_diagram_html, _edge_geometry, _free_arrow_geometry

ROOT = Path(__file__).resolve().parent.parent
ALLOWED_TAGS = {'svg', 'defs', 'g', 'path', 'rect', 'ellipse', 'circle', 'text',
                'tspan', 'polygon', 'polyline', 'line', 'marker', 'pattern', 'mask', 'clipPath'}


def _fit_export_viewbox(root, payload):
    from reportlab.graphics.svgpath import SvgPath

    boxes = []
    for node in payload['nodes']:
        boxes.append((node['x'] - node['width'] / 2, node['y'] - node['height'] / 2,
                      node['x'] + node['width'] / 2, node['y'] + node['height'] / 2))
    for element in root.xpath('.//*[not(ancestor::defs)]'):
        if element.tag == 'path':
            bounds = SvgPath(element.get('d', '')).getBounds()
            if bounds:
                boxes.append(bounds)
        elif element.tag == 'rect':
            x, y = float(element.get('x', 0)), float(element.get('y', 0))
            boxes.append((x, y, x + float(element.get('width', 0)), y + float(element.get('height', 0))))
        elif element.tag in {'text', 'tspan'} and element.get('x') is not None and element.text:
            x, y = float(element.get('x')), float(element.get('y', 0))
            parent = element.getparent() if element.tag == 'tspan' else element
            size = re.search(r'font-size:([\d.]+)', parent.get('style', ''))
            font_size = float(size.group(1)) if size else 15
            half_width = len(element.text) * font_size * .35
            boxes.append((x - half_width, y - font_size, x + half_width, y + font_size))
    for stroke in payload['strokes']:
        for x, y in stroke['points']:
            boxes.append((x - stroke['width'], y - stroke['width'], x + stroke['width'], y + stroke['width']))
    if boxes:
        left, top = min(b[0] for b in boxes) - 24, min(b[1] for b in boxes) - 24
        right, bottom = max(b[2] for b in boxes) + 24, max(b[3] for b in boxes) + 24
        root.set('viewBox', f'{left} {top} {right - left} {bottom - top}')


def diagram_document_data(encoded):
    payload = decode_diagram_payload(encoded)
    if not payload:
        return None
    html = render_diagram_html(payload, encoded)
    fragment = html[html.index('<svg '):html.index('</svg>') + 6]
    root = etree.fromstring(fragment.encode(), etree.XMLParser(resolve_entities=False, no_network=True))
    for element in list(root.iter()):
        if element.tag not in ALLOWED_TAGS:
            raise ValueError('Unsupported diagram element')
        for attribute in list(element.attrib):
            if attribute.startswith(('data-', 'aria-', 'on')) or attribute in {'tabindex', 'role', 'href'}:
                del element.attrib[attribute]
        if 'answer-diagram-edge-hit' in element.get('class', '').split():
            element.getparent().remove(element)

    notes = []
    nodes = {node['id']: node for node in payload['nodes']}
    edge_pairs = {(edge['from'], edge['to']) for edge in payload['edges']}
    edge_groups = root.xpath('.//g[contains(concat(" ", @class, " "), " answer-diagram-edge-group ")]')
    for index, edge in enumerate(payload['edges'] + payload['arrows']):
        if not edge['description']:
            continue
        number = len(notes) + 1
        label = edge['label'] or 'Bağlantı'
        if 'from' in edge:
            source = nodes[edge['from']]['label'] or 'Adsız öğe'
            target = nodes[edge['to']]['label'] or 'Adsız öğe'
            label = f'{source} → {target}: {label}'
        notes.append((f'[{number}] {label}', edge['description']))
        group = edge_groups[index]
        text = group.find('.//text')
        if text is not None:
            text.text = f'{text.text or ""} [{number}]'
            background = group.find('.//rect')
            if background is not None:
                background.set('width', str(float(background.get('width')) + 40))
                background.set('x', str(float(background.get('x')) - 20))
        else:
            if 'from' in edge:
                has_reverse = edge['from'] != edge['to'] and (edge['to'], edge['from']) in edge_pairs
                geometry = _edge_geometry(
                    nodes[edge['from']], nodes[edge['to']], payload['nodes'],
                    edge['route'], edge['bend'], has_reverse=has_reverse,
                    reverse_bend=has_reverse and edge['from'] > edge['to'],
                )
            else:
                geometry = _free_arrow_geometry(edge, nodes, {r['id']: r for r in payload['regions']})
            x, y = geometry['label_x'], geometry['label_y']
            etree.SubElement(group, 'rect', {'x': str(x - 19), 'y': str(y - 17), 'width': '38', 'height': '24', 'rx': '4', 'class': 'answer-diagram-edge-label-bg'})
            etree.SubElement(group, 'text', {'x': str(x), 'y': str(y), 'class': 'answer-diagram-edge-label'}).text = f'[{number}]'
    for node in payload['nodes']:
        if node['href']:
            notes.append((node['label'] or 'Bağlantılı öğe', node['href']))
        if len(node['label']) > 180:
            notes.append(('Öğe metni', node['label']))

    root.set('xmlns', 'http://www.w3.org/2000/svg')
    _fit_export_viewbox(root, payload)
    _, _, width, height = map(float, root.get('viewBox').split())
    scale = min(2, 2200 / max(width, height))
    root.set('width', str(max(1, round(width * scale))))
    root.set('height', str(max(1, round(height * scale))))
    return payload, etree.tostring(root, encoding='unicode'), notes


def diagram_png(svg):
    import resvg_py
    rendered = resvg_py.svg_to_bytes(
        svg_string=svg, background='#ffffff', skip_system_fonts=True,
        font_files=[str(ROOT / 'static/fonts/DejaVuSans.ttf'), str(ROOT / 'static/fonts/DejaVuSans-Bold.ttf')],
        font_family='DejaVu Sans',
        style_sheet=(ROOT / 'static/css/diagram_paper.css').read_text(encoding='utf-8'),
    )
    with Image.open(BytesIO(rendered)) as image:
        rgb = image.convert('RGB')
        bounds = ImageChops.difference(rgb, Image.new('RGB', rgb.size, 'white')).getbbox()
        if bounds:
            rgb = ImageOps.expand(rgb.crop(bounds), border=12, fill='white')
        output = BytesIO()
        rgb.save(output, format='PNG')
        return output.getvalue()
