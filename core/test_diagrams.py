import base64
import json

from django.test import SimpleTestCase

from core.diagram_markup import (
    _resolved_free_arrow_endpoints,
    decode_diagram_payload,
    encode_diagram_payload,
    normalize_diagram_payload,
)
from core.templatetags.custom_tags import safe_markdownify, truncate_math_safe


class DiagramMarkupTests(SimpleTestCase):
    def setUp(self):
        self.payload = {
            "version": 1,
            "title": "Karar döngüsü",
            "nodes": [
                {
                    "id": "n1",
                    "label": "Başlangıç",
                    "shape": "terminal",
                    "x": 150,
                    "y": 270,
                },
                {
                    "id": "n2",
                    "label": "Kontrol et",
                    "shape": "decision",
                    "x": 500,
                    "y": 180,
                },
                {
                    "id": "n3",
                    "label": "Yeniden düzenle",
                    "shape": "process",
                    "x": 770,
                    "y": 330,
                },
            ],
            "edges": [
                {"from": "n1", "to": "n2"},
                {"from": "n2", "to": "n3"},
                {"from": "n3", "to": "n2"},
            ],
        }

    def test_payload_round_trip_preserves_cycle(self):
        encoded = encode_diagram_payload(self.payload)
        decoded = decode_diagram_payload(encoded)

        self.assertEqual(decoded["title"], "Karar döngüsü")
        self.assertEqual(len(decoded["nodes"]), 3)
        reverse_edge = next(edge for edge in decoded["edges"] if edge["from"] == "n3")
        self.assertEqual(reverse_edge["to"], "n2")
        self.assertEqual(reverse_edge["route"], "auto")
        self.assertEqual(reverse_edge["description"], "")
        self.assertEqual(decoded["version"], 5)
        self.assertEqual(decoded["nodes"][0]["tone"], "neutral")
        self.assertEqual(decoded["nodes"][0]["width"], 152)

    def test_new_markers_use_compact_embedded_payload(self):
        encoded = encode_diagram_payload(self.payload)
        padding = "=" * (-len(encoded) % 4)
        packed = json.loads(base64.urlsafe_b64decode(encoded + padding).decode("utf-8"))

        self.assertIn("n", packed)
        self.assertIn("e", packed)
        self.assertNotIn("nodes", packed)
        self.assertLess(len(encoded), 700)

    def test_version_one_full_json_markers_remain_readable(self):
        raw = json.dumps(self.payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        encoded = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")

        decoded = decode_diagram_payload(encoded)

        self.assertEqual(decoded["title"], "Karar döngüsü")
        self.assertEqual(len(decoded["nodes"]), 3)
        self.assertEqual(decoded["version"], 5)

    def test_malformed_payload_is_ignored(self):
        self.assertIsNone(decode_diagram_payload("invalid_base64_payload"))

    def test_markdown_renders_clickable_svg(self):
        marker = f"[[diyagram:{encode_diagram_payload(self.payload)}]]"

        rendered = str(safe_markdownify(marker))

        self.assertIn('class="answer-diagram"', rendered)
        self.assertIn('class="answer-diagram-open"', rendered)
        self.assertIn('class="answer-diagram-toggle"', rendered)
        self.assertIn('class="answer-diagram-body"', rendered)
        self.assertIn('data-diagram-id="', rendered)
        self.assertIn('<svg viewBox="0 0 960 540"', rendered)
        self.assertIn('Karar döngüsü', rendered)
        self.assertEqual(rendered.count('class="answer-diagram-edge"'), 3)

    def test_labels_are_escaped_before_svg_rendering(self):
        self.payload["nodes"][0]["label"] = '<script>alert("x")</script>'
        marker = f"[[diyagram:{encode_diagram_payload(self.payload)}]]"

        rendered = str(safe_markdownify(marker))

        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)

    def test_invalid_nodes_and_edges_are_rejected_or_removed(self):
        payload = dict(self.payload)
        payload["nodes"] = [dict(node) for node in self.payload["nodes"]]
        payload["nodes"][0]["shape"] = "unsafe"
        payload["nodes"][0]["x"] = -200
        payload["edges"] = [{"from": "n1", "to": "missing"}]

        normalized = normalize_diagram_payload(payload)

        self.assertEqual(normalized["nodes"][0]["shape"], "process")
        self.assertEqual(normalized["nodes"][0]["x"], 84)
        self.assertEqual(normalized["edges"], [])

    def test_v2_styles_and_edge_labels_are_rendered_safely(self):
        self.payload["nodes"][0]["shape"] = "document"
        self.payload["nodes"][0]["tone"] = "blue"
        self.payload["edges"][0]["label"] = '<Evet & devam>'
        self.payload["edges"][0]["style"] = "dashed"
        marker = f"[[diyagram:{encode_diagram_payload(self.payload)}]]"

        rendered = str(safe_markdownify(marker))

        self.assertIn("answer-diagram-node-document", rendered)
        self.assertIn("answer-diagram-tone-blue", rendered)
        self.assertIn("answer-diagram-edge-dashed", rendered)
        self.assertIn("answer-diagram-edge-label-bg", rendered)
        self.assertIn("&lt;Evet &amp; devam&gt;", rendered)
        self.assertNotIn("<Evet & devam>", rendered)

    def test_unknown_v2_styles_fall_back_to_safe_defaults(self):
        self.payload["nodes"][0]["tone"] = "javascript:alert(1)"
        self.payload["edges"][0]["style"] = "unsafe"

        normalized = normalize_diagram_payload(self.payload)

        self.assertEqual(normalized["nodes"][0]["tone"], "neutral")
        self.assertEqual(normalized["edges"][0]["style"], "solid")

    def test_v3_node_sizes_links_groups_and_edge_details_round_trip(self):
        self.payload["uid"] = "diagram-test-1"
        self.payload["nodes"][0].update(
            {
                "label": "Uzun ve ayrıntılı bir başlangıç açıklaması",
                "width": 280,
                "height": 120,
                "href": "/baslangic/",
            }
        )
        self.payload["edges"][0].update(
            {
                "label": "Bu nedenle",
                "description": "İlk durumdan kontrole geçişin\nikinci satırı.",
                "route": "curve",
                "bend": 72,
            }
        )
        self.payload["groups"] = [
            {"id": "g1", "label": "Hazırlık", "tone": "blue", "node_ids": ["n1", "n2"]}
        ]

        decoded = decode_diagram_payload(encode_diagram_payload(self.payload))
        marker = f"[[diyagram:{encode_diagram_payload(self.payload)}]]"
        rendered = str(safe_markdownify(marker))

        self.assertEqual(decoded["uid"], "diagram-test-1")
        self.assertEqual(decoded["nodes"][0]["width"], 280)
        self.assertEqual(decoded["nodes"][0]["height"], 120)
        self.assertEqual(decoded["nodes"][0]["href"], "/baslangic/")
        self.assertEqual(decoded["edges"][0]["route"], "curve")
        self.assertEqual(decoded["edges"][0]["bend"], 72)
        self.assertIn("\n", decoded["edges"][0]["description"])
        self.assertEqual(decoded["groups"][0]["node_ids"], ["n1", "n2"])
        self.assertIn("answer-diagram-node-linked", rendered)
        self.assertIn("answer-diagram-node-link-indicator", rendered)

    def test_unsafe_links_and_group_members_are_filtered(self):
        self.payload["nodes"][0]["href"] = "javascript:alert(1)"
        self.payload["nodes"][1]["href"] = "https://example.com/path"
        self.payload["groups"] = [
            {"id": "g1", "label": "Geçerli", "node_ids": ["n1", "missing", "n2"]},
            {"id": "g2", "label": "Tek düğüm", "node_ids": ["n3"]},
        ]

        normalized = normalize_diagram_payload(self.payload)

        self.assertEqual(normalized["nodes"][0]["href"], "")
        self.assertEqual(normalized["nodes"][1]["href"], "https://example.com/path")
        self.assertEqual(len(normalized["groups"]), 1)
        self.assertEqual(normalized["groups"][0]["node_ids"], ["n1", "n2"])

    def test_edge_explanation_and_group_are_rendered_safely(self):
        self.payload["edges"][0].update(
            {
                "label": "X oku",
                "description": '<img src=x onerror="alert(1)"> açıklaması',
                "route": "orthogonal",
                "bend": 36,
            }
        )
        self.payload["groups"] = [
            {"id": "g1", "label": "Aşama <1>", "tone": "gold", "node_ids": ["n1", "n2"]}
        ]
        marker = f"[[diyagram:{encode_diagram_payload(self.payload)}]]"

        rendered = str(safe_markdownify(marker))

        self.assertIn("answer-diagram-edge-interactive", rendered)
        self.assertIn('data-diagram-edge-index="0"', rendered)
        self.assertIn('data-diagram-edge-label="X oku"', rendered)
        self.assertIn("&lt;img src=x onerror=&quot;alert(1)&quot;&gt; açıklaması", rendered)
        self.assertNotIn("<img src=x", rendered)
        self.assertIn("answer-diagram-group-gold", rendered)
        self.assertIn("Aşama &lt;1&gt;", rendered)

    def test_large_diagrams_keep_world_coordinates_and_expand_viewbox(self):
        self.payload["nodes"][0].update({"x": 2200, "y": 1100, "width": 600, "height": 300})

        normalized = normalize_diagram_payload(self.payload)
        marker = f"[[diyagram:{encode_diagram_payload(self.payload)}]]"
        rendered = str(safe_markdownify(marker))

        self.assertEqual(normalized["nodes"][0]["x"], 2200)
        self.assertEqual(normalized["nodes"][0]["y"], 1100)
        self.assertEqual(normalized["nodes"][0]["width"], 600)
        self.assertEqual(normalized["nodes"][0]["height"], 300)
        self.assertNotIn('<svg viewBox="0 0 960 540"', rendered)

    def test_pyramid_and_set_shapes_render_without_connections(self):
        payload = {
            "title": "Kavramsal görünüm",
            "nodes": [
                {
                    "id": "n1",
                    "label": "Temel",
                    "shape": "pyramid",
                    "tone": "gold",
                    "x": 350,
                    "y": 270,
                    "width": 320,
                    "height": 110,
                },
                {
                    "id": "n2",
                    "label": "Küme A",
                    "shape": "set",
                    "tone": "blue",
                    "x": 640,
                    "y": 270,
                    "width": 260,
                    "height": 220,
                },
            ],
            "edges": [],
        }
        marker = f"[[diyagram:{encode_diagram_payload(payload)}]]"

        rendered = str(safe_markdownify(marker))

        self.assertIn("answer-diagram-node-pyramid", rendered)
        self.assertIn("answer-diagram-node-set", rendered)
        self.assertIn("<ellipse", rendered)
        self.assertIn("<polygon", rendered)

    def test_resizable_sets_region_labels_and_extended_curves_round_trip(self):
        payload = {
            "uid": "sets-extended",
            "title": "Kümeler",
            "nodes": [
                {
                    "id": "set-a",
                    "label": "A",
                    "shape": "set",
                    "tone": "blue",
                    "x": 620,
                    "y": 520,
                    "width": 900,
                    "height": 700,
                },
                {
                    "id": "set-b",
                    "label": "B",
                    "shape": "set",
                    "tone": "green",
                    "x": 980,
                    "y": 520,
                    "width": 760,
                    "height": 640,
                },
                {
                    "id": "intersection",
                    "label": "A ∩ B",
                    "shape": "label",
                    "x": 800,
                    "y": 520,
                    "width": 220,
                    "height": 64,
                },
                {
                    "id": "result",
                    "label": "Sonuç",
                    "shape": "process",
                    "x": 1700,
                    "y": 520,
                },
            ],
            "edges": [
                {
                    "from": "intersection",
                    "to": "result",
                    "route": "curve",
                    "bend": 440,
                    "label": "yorumlanır",
                    "description": "Kesişimden çıkan sonuç.",
                }
            ],
        }

        decoded = decode_diagram_payload(encode_diagram_payload(payload))
        marker = f"[[diyagram:{encode_diagram_payload(payload)}]]"
        rendered = str(safe_markdownify(marker))

        self.assertEqual(decoded["nodes"][0]["width"], 900)
        self.assertEqual(decoded["nodes"][0]["height"], 700)
        self.assertEqual(decoded["nodes"][2]["shape"], "label")
        self.assertEqual(decoded["edges"][0]["bend"], 440)
        self.assertIn("answer-diagram-node-label", rendered)
        self.assertIn("A ∩ B", rendered)

    def test_named_hatched_regions_and_font_sizes_round_trip(self):
        payload = {
            "uid": "region-diagram",
            "title": "Küme işlemleri",
            "nodes": [
                {
                    "id": "a",
                    "label": "",
                    "shape": "set",
                    "tone": "green",
                    "x": 400,
                    "y": 350,
                    "width": 520,
                    "height": 460,
                    "font_size": 28,
                },
                {
                    "id": "b",
                    "label": "B",
                    "shape": "process",
                    "tone": "blue",
                    "x": 620,
                    "y": 350,
                    "width": 520,
                    "height": 360,
                    "font_size": 22,
                },
            ],
            "edges": [],
            "regions": [
                {
                    "id": "shared",
                    "label": "Ortak alan",
                    "operation": "intersection",
                    "tone": "gold",
                    "node_ids": ["a", "b"],
                },
                {
                    "id": "combined",
                    "label": "Birleşik alan",
                    "operation": "union",
                    "tone": "blue",
                    "node_ids": ["a", "b"],
                },
            ],
        }

        decoded = decode_diagram_payload(encode_diagram_payload(payload))
        marker = f"[[diyagram:{encode_diagram_payload(payload)}]]"
        rendered = str(safe_markdownify(marker))

        self.assertEqual(decoded["nodes"][0]["label"], "")
        self.assertEqual(decoded["nodes"][0]["font_size"], 28)
        self.assertEqual(decoded["regions"][0]["operation"], "intersection")
        self.assertEqual(decoded["regions"][1]["operation"], "union")
        self.assertIn("answer-diagram-regions", rendered)
        self.assertIn("answer-diagram-region-intersection", rendered)
        self.assertIn("answer-diagram-region-union", rendered)
        self.assertIn("Ortak alan", rendered)
        self.assertIn("Birleşik alan", rendered)
        self.assertIn("font-size:28.0px", rendered)

    def test_node_label_offsets_round_trip_and_render_in_published_svg(self):
        payload = {
            "uid": "movable-labels",
            "title": "Taşınan yazılar",
            "nodes": [
                {
                    "id": "set-a",
                    "label": "A kümesi",
                    "shape": "set",
                    "tone": "green",
                    "x": 400,
                    "y": 300,
                    "width": 420,
                    "height": 300,
                    "font_size": 18,
                    "label_offset_x": -70,
                    "label_offset_y": 45,
                }
            ],
            "edges": [],
        }

        decoded = decode_diagram_payload(encode_diagram_payload(payload))
        rendered = str(safe_markdownify(f"[[diyagram:{encode_diagram_payload(payload)}]]"))

        self.assertEqual(decoded["nodes"][0]["label_offset_x"], -70)
        self.assertEqual(decoded["nodes"][0]["label_offset_y"], 45)
        self.assertIn('<tspan x="330.0" y="345.0">A kümesi</tspan>', rendered)

    def test_region_label_offsets_round_trip_and_render_without_a_box(self):
        payload = {
            "uid": "movable-region-label",
            "title": "Taşınan kesişim adı",
            "nodes": [
                {
                    "id": "a",
                    "label": "A",
                    "shape": "set",
                    "x": 400,
                    "y": 300,
                    "width": 300,
                    "height": 240,
                },
                {
                    "id": "b",
                    "label": "B",
                    "shape": "set",
                    "x": 500,
                    "y": 300,
                    "width": 300,
                    "height": 240,
                },
            ],
            "edges": [],
            "regions": [
                {
                    "id": "shared",
                    "label": "Ortak isim",
                    "operation": "intersection",
                    "tone": "gold",
                    "node_ids": ["a", "b"],
                    "label_offset_x": 60,
                    "label_offset_y": -40,
                }
            ],
        }

        decoded = decode_diagram_payload(encode_diagram_payload(payload))
        rendered = str(safe_markdownify(f"[[diyagram:{encode_diagram_payload(payload)}]]"))

        self.assertEqual(decoded["regions"][0]["label_offset_x"], 60)
        self.assertEqual(decoded["regions"][0]["label_offset_y"], -40)
        self.assertIn(
            '<g class="answer-diagram-region-label"><text x="510.0" y="261.0">Ortak isim</text></g>',
            rendered,
        )
        self.assertNotIn('<g class="answer-diagram-region-label"><rect', rendered)

    def test_difference_region_keeps_selected_base_as_first_member(self):
        payload = {
            "title": "Yönlü fark",
            "nodes": [
                {
                    "id": "a",
                    "label": "A",
                    "shape": "process",
                    "x": 400,
                    "y": 300,
                    "width": 300,
                    "height": 220,
                },
                {
                    "id": "b",
                    "label": "B",
                    "shape": "set",
                    "x": 520,
                    "y": 300,
                    "width": 300,
                    "height": 220,
                },
            ],
            "edges": [],
            "regions": [
                {
                    "id": "b-minus-a",
                    "label": "Yalnız B",
                    "operation": "difference",
                    "node_ids": ["b", "a"],
                }
            ],
        }

        decoded = decode_diagram_payload(encode_diagram_payload(payload))
        rendered = str(safe_markdownify(f"[[diyagram:{encode_diagram_payload(payload)}]]"))

        self.assertEqual(decoded["regions"][0]["node_ids"], ["b", "a"])
        self.assertRegex(rendered, r'<mask[^>]+>.*?<ellipse[^>]+fill="white"')

    def test_difference_region_filters_missing_members_and_supports_large_shapes(self):
        payload = {
            "title": "Fark",
            "nodes": [
                {
                    "id": "a",
                    "label": "A",
                    "shape": "process",
                    "x": 1800,
                    "y": 1200,
                    "width": 2200,
                    "height": 1600,
                },
                {
                    "id": "b",
                    "label": "B",
                    "shape": "decision",
                    "x": 2100,
                    "y": 1200,
                    "width": 800,
                    "height": 700,
                },
            ],
            "edges": [],
            "regions": [
                {
                    "id": "difference",
                    "label": "Yalnız A",
                    "operation": "difference",
                    "node_ids": ["a", "missing", "b"],
                }
            ],
        }

        decoded = decode_diagram_payload(encode_diagram_payload(payload))
        rendered = str(safe_markdownify(f"[[diyagram:{encode_diagram_payload(payload)}]]"))

        self.assertEqual(decoded["nodes"][0]["width"], 2200)
        self.assertEqual(decoded["nodes"][0]["height"], 1600)
        self.assertEqual(decoded["regions"][0]["node_ids"], ["a", "b"])
        self.assertIn("answer-diagram-region-difference", rendered)
        self.assertIn("diagram-region-mask-", rendered)

    def test_old_compact_v2_payload_remains_readable(self):
        packed = {
            "v": 2,
            "t": "Eski kompakt diyagram",
            "n": [
                ["n1", "Başla", "terminal", "green", 140, 270],
                ["n2", "Bitir", "process", "neutral", 650, 270],
            ],
            "e": [["n1", "n2", "Sonra", "solid"]],
        }
        raw = json.dumps(packed, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        encoded = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")

        decoded = decode_diagram_payload(encoded)

        self.assertEqual(decoded["version"], 5)
        self.assertEqual(decoded["nodes"][0]["width"], 152)
        self.assertEqual(decoded["edges"][0]["description"], "")

    def test_truncated_preview_never_exposes_partial_diagram_data(self):
        marker = f"[[diyagram:{encode_diagram_payload(self.payload)}]]"
        raw_text = f"Önceki paragraf.\n\n{marker}\n\nSonraki paragraf."

        preview = truncate_math_safe(raw_text, 180)

        self.assertEqual(preview, "Önceki paragraf.")
        self.assertNotIn("[[diyagram:", preview)

    def test_independent_arrow_only_diagram_round_trips_and_renders(self):
        payload = {
            "uid": "free-arrow-only",
            "title": "Bağımsız açıklama",
            "nodes": [],
            "edges": [],
            "arrows": [
                {
                    "id": "a1",
                    "start_x": 180,
                    "start_y": 310,
                    "end_x": 760,
                    "end_y": 210,
                    "label": "Etkiler",
                    "style": "dashed",
                    "description": "Bu ok iki bağımsız alan arasındaki ilişkiyi açıklar.",
                    "route": "curve",
                    "bend": 180,
                }
            ],
        }

        encoded = encode_diagram_payload(payload)
        decoded = decode_diagram_payload(encoded)
        rendered = str(safe_markdownify(f"[[diyagram:{encoded}]]"))

        self.assertEqual(decoded["version"], 5)
        self.assertEqual(decoded["nodes"], [])
        self.assertEqual(decoded["arrows"][0]["bend"], 180)
        self.assertIn("answer-diagram-free-arrow-group", rendered)
        self.assertIn("answer-diagram-edge-dashed", rendered)
        self.assertIn("answer-diagram-edge-interactive", rendered)
        self.assertIn("Etkiler", rendered)

    def test_blank_region_label_does_not_publish_generated_name(self):
        payload = {
            "title": "Adsız kesişim",
            "nodes": [
                {
                    "id": "a",
                    "label": "A",
                    "shape": "set",
                    "x": 390,
                    "y": 270,
                    "width": 300,
                    "height": 240,
                },
                {
                    "id": "b",
                    "label": "B",
                    "shape": "set",
                    "x": 550,
                    "y": 270,
                    "width": 300,
                    "height": 240,
                },
            ],
            "edges": [],
            "regions": [
                {
                    "id": "shared",
                    "label": "",
                    "operation": "intersection",
                    "node_ids": ["a", "b"],
                }
            ],
        }

        encoded = encode_diagram_payload(payload)
        rendered = str(safe_markdownify(f"[[diyagram:{encoded}]]"))

        self.assertIn("answer-diagram-region-intersection", rendered)
        self.assertIn("answer-diagram-region-shape", rendered)
        self.assertNotIn("answer-diagram-region-label", rendered)
        self.assertNotIn("A ∩ B", rendered)

    def test_non_overlapping_intersection_is_not_rendered(self):
        payload = {
            "title": "Ayrık kümeler",
            "nodes": [
                {
                    "id": "a",
                    "label": "A",
                    "shape": "set",
                    "x": 220,
                    "y": 270,
                    "width": 220,
                    "height": 180,
                },
                {
                    "id": "b",
                    "label": "B",
                    "shape": "set",
                    "x": 740,
                    "y": 270,
                    "width": 220,
                    "height": 180,
                },
            ],
            "edges": [],
            "regions": [
                {
                    "id": "shared",
                    "label": "Eski kesişim",
                    "operation": "intersection",
                    "node_ids": ["a", "b"],
                }
            ],
        }

        encoded = encode_diagram_payload(payload)
        decoded = decode_diagram_payload(encoded)
        rendered = str(safe_markdownify(f"[[diyagram:{encoded}]]"))

        self.assertEqual(decoded["regions"][0]["id"], "shared")
        self.assertNotIn("answer-diagram-region-intersection", rendered)
        self.assertNotIn("Eski kesişim", rendered)

    def test_independent_arrow_anchors_round_trip_and_follow_region(self):
        payload = {
            "uid": "anchored-arrow",
            "title": "Bağlı ok",
            "nodes": [
                {
                    "id": "a",
                    "label": "A",
                    "shape": "set",
                    "x": 300,
                    "y": 270,
                    "width": 280,
                    "height": 220,
                },
                {
                    "id": "b",
                    "label": "B",
                    "shape": "set",
                    "x": 430,
                    "y": 270,
                    "width": 280,
                    "height": 220,
                },
                {
                    "id": "result",
                    "label": "Sonuç",
                    "shape": "process",
                    "x": 760,
                    "y": 270,
                    "width": 180,
                    "height": 80,
                },
            ],
            "edges": [],
            "regions": [
                {
                    "id": "shared",
                    "label": "Ortak alan",
                    "operation": "intersection",
                    "node_ids": ["a", "b"],
                }
            ],
            "arrows": [
                {
                    "id": "a1",
                    "start_x": 24,
                    "start_y": 24,
                    "end_x": 900,
                    "end_y": 500,
                    "start_anchor": "r:shared",
                    "end_anchor": "n:result",
                    "route": "straight",
                }
            ],
        }

        encoded = encode_diagram_payload(payload)
        decoded = decode_diagram_payload(encoded)
        rendered = str(safe_markdownify(f"[[diyagram:{encoded}]]"))

        self.assertEqual(decoded["arrows"][0]["start_anchor"], "r:shared")
        self.assertEqual(decoded["arrows"][0]["end_anchor"], "n:result")
        self.assertIn("answer-diagram-free-arrow-group", rendered)
        self.assertNotIn('d="M 24.0 24.0', rendered)

    def test_anchored_free_arrow_starts_at_region_center_and_ends_at_node_boundary(self):
        payload = {
            "uid": "centered-anchors",
            "title": "Merkez bağlantısı",
            "nodes": [
                {
                    "id": "step",
                    "label": "Yeni adım",
                    "shape": "process",
                    "x": 500,
                    "y": 300,
                    "width": 480,
                    "height": 200,
                },
                {
                    "id": "decision",
                    "label": "Karar",
                    "shape": "decision",
                    "x": 800,
                    "y": 300,
                    "width": 300,
                    "height": 280,
                },
                {
                    "id": "result",
                    "label": "Sonuç",
                    "shape": "terminal",
                    "x": 695,
                    "y": 700,
                    "width": 180,
                    "height": 80,
                },
            ],
            "edges": [],
            "regions": [
                {
                    "id": "shared",
                    "label": "",
                    "operation": "intersection",
                    "node_ids": ["step", "decision"],
                }
            ],
            "arrows": [
                {
                    "id": "a1",
                    "start_x": 24,
                    "start_y": 24,
                    "end_x": 695,
                    "end_y": 700,
                    "start_anchor": "r:shared",
                    "end_anchor": "n:result",
                    "route": "straight",
                }
            ],
        }

        decoded = decode_diagram_payload(encode_diagram_payload(payload))
        nodes_by_id = {node["id"]: node for node in decoded["nodes"]}
        regions_by_id = {region["id"]: region for region in decoded["regions"]}
        start, end = _resolved_free_arrow_endpoints(
            decoded["arrows"][0],
            nodes_by_id,
            regions_by_id,
        )
        rendered = str(safe_markdownify(f"[[diyagram:{encode_diagram_payload(payload)}]]"))

        self.assertEqual(start, (695, 300))
        self.assertEqual(end, (695, 660))
        self.assertIn('d="M 695.0 300.0 L 695.0 660.0"', rendered)

    def test_invalid_independent_arrow_anchors_are_removed(self):
        payload = {
            "title": "Geçersiz çıpa",
            "nodes": [
                {"id": "n1", "label": "Bir", "shape": "process", "x": 200, "y": 270}
            ],
            "edges": [],
            "arrows": [
                {
                    "id": "a1",
                    "start_x": 100,
                    "start_y": 100,
                    "end_x": 500,
                    "end_y": 300,
                    "start_anchor": "n:missing",
                    "end_anchor": "r:missing",
                }
            ],
        }

        normalized = normalize_diagram_payload(payload)

        self.assertEqual(normalized["arrows"][0]["start_anchor"], "")
        self.assertEqual(normalized["arrows"][0]["end_anchor"], "")

    def test_compact_v4_payload_without_independent_arrows_remains_readable(self):
        packed = {
            "v": 4,
            "i": "legacy-v4",
            "t": "Dördüncü sürüm",
            "n": [
                ["n1", "Başla", "terminal", "green", 160, 270, 160, 68, "", 15],
                ["n2", "Bitir", "terminal", "blue", 720, 270, 160, 68, "", 15],
            ],
            "e": [["n1", "n2", "", "solid", "", "auto", 0]],
            "g": [],
            "r": [["r1", "Eski bölge", "union", "gold", ["n1", "n2"]]],
        }
        raw = json.dumps(packed, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        encoded = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")

        decoded = decode_diagram_payload(encoded)

        self.assertEqual(decoded["version"], 5)
        self.assertEqual(decoded["arrows"], [])
        self.assertEqual(len(decoded["edges"]), 1)
        self.assertEqual(decoded["nodes"][0]["label_offset_x"], 0)
        self.assertEqual(decoded["nodes"][0]["label_offset_y"], 0)
        self.assertEqual(decoded["regions"][0]["label_offset_x"], 0)
        self.assertEqual(decoded["regions"][0]["label_offset_y"], 0)
