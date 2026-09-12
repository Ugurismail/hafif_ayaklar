from io import BytesIO
from django.test import SimpleTestCase
from lxml import etree
from PIL import Image, ImageChops
from .diagram_markup import encode_diagram_payload, _edge_geometry
from .diagram_export import diagram_document_data, diagram_png


class DiagramExportTests(SimpleTestCase):
    def test_renderer_is_bounded_nonblank_and_does_not_include_active_content(self):
        encoded = encode_diagram_payload({
            'title': 'Türkçe çizim',
            'nodes': [{'id': 'a', 'label': '<script>alert(1)</script> ŞĞı', 'x': 200, 'y': 200,
                       'shape': 'set', 'tone': 'blue', 'href': 'javascript:alert(1)'}],
            'edges': [],
        })
        payload, svg, notes = diagram_document_data(encoded)
        root = etree.fromstring(svg.encode())
        self.assertFalse(root.xpath('//*[local-name()="script" or local-name()="image" or @href]'))
        self.assertNotIn('javascript:', svg)
        self.assertEqual(notes, [])
        image = Image.open(BytesIO(diagram_png(svg))).convert('RGB')
        self.assertLessEqual(max(image.size), 2200)
        self.assertIsNotNone(ImageChops.difference(image, Image.new('RGB', image.size, 'white')).getbbox())

    def test_invalid_payload_has_no_image(self):
        self.assertIsNone(diagram_document_data('abc'))

    def test_large_curve_and_freehand_strokes_fit_inside_export(self):
        encoded = encode_diagram_payload({
            'nodes': [
                {'id': 'a', 'label': 'A', 'x': 200, 'y': 200},
                {'id': 'b', 'label': 'B', 'x': 800, 'y': 200},
            ],
            'edges': [{'from': 'a', 'to': 'b', 'route': 'curve', 'bend': 1200}],
            'strokes': [{'id': 's', 'points': [[100, 1800], [900, 1900]], 'width': 8}],
        })
        _, svg, _ = diagram_document_data(encoded)
        root = etree.fromstring(svg.encode())
        left, top, width, height = map(float, root.get('viewBox').split())
        self.assertLessEqual(top, 150)
        self.assertGreaterEqual(top + height, 1908)
        self.assertGreaterEqual(left + width, 908)
        self.assertEqual(len(root.xpath('//*[local-name()="polyline"]')), 1)
        image = Image.open(BytesIO(diagram_png(svg))).convert('RGB')
        self.assertLessEqual(max(image.size), 2200)
        self.assertIsNotNone(ImageChops.difference(image, Image.new('RGB', image.size, 'white')).getbbox())

    def test_unlabelled_reverse_edges_keep_notes_on_their_own_curves(self):
        encoded = encode_diagram_payload({
            'nodes': [
                {'id': 'a', 'label': 'A', 'x': 200, 'y': 200},
                {'id': 'b', 'label': 'B', 'x': 800, 'y': 200},
            ],
            'edges': [
                {'from': 'a', 'to': 'b', 'description': 'Forward'},
                {'from': 'b', 'to': 'a', 'description': 'Return'},
            ],
        })
        payload, svg, notes = diagram_document_data(encoded)
        root = etree.fromstring(svg.encode())
        labels = root.xpath('//*[local-name()="text" and @class="answer-diagram-edge-label"]')
        self.assertEqual(len(notes), 2)
        nodes = {node['id']: node for node in payload['nodes']}
        for edge, label in zip(payload['edges'], labels):
            geometry = _edge_geometry(
                nodes[edge['from']], nodes[edge['to']], payload['nodes'],
                edge['route'], edge['bend'], has_reverse=True,
                reverse_bend=edge['from'] > edge['to'],
            )
            self.assertAlmostEqual(float(label.get('x')), geometry['label_x'])
            self.assertAlmostEqual(float(label.get('y')), geometry['label_y'])
