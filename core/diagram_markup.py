import base64
import binascii
import hashlib
import json
import math
from functools import lru_cache
from textwrap import wrap
from urllib.parse import urlsplit

from django.utils.html import escape


DIAGRAM_MARKER_PATTERN = r"\[\[diyagram:([A-Za-z0-9_-]{1,64000})\]\]"
CANVAS_WIDTH = 8000
CANVAS_HEIGHT = 5200
VIEWPORT_WIDTH = 960
VIEWPORT_HEIGHT = 540
MIN_NODE_WIDTH = 80
MIN_NODE_HEIGHT = 44
MAX_NODE_WIDTH = 2400
MAX_NODE_HEIGHT = 1800
MIN_FONT_SIZE = 10
MAX_FONT_SIZE = 52
MAX_EDGE_BEND = 1200
MAX_NODES = 80
MAX_EDGES = 200
MAX_FREE_ARROWS = 100
MAX_GROUPS = 32
MAX_REGIONS = 40
ALLOWED_SHAPES = {
    "process",
    "decision",
    "terminal",
    "document",
    "data",
    "pyramid",
    "set",
    "label",
}
ALLOWED_TONES = {"neutral", "green", "blue", "gold", "red"}
ALLOWED_EDGE_STYLES = {"solid", "dashed"}
ALLOWED_EDGE_ROUTES = {"auto", "straight", "curve", "orthogonal"}
ALLOWED_REGION_OPERATIONS = {"intersection", "union", "difference"}


def encode_diagram_payload(payload):
    normalized = normalize_diagram_payload(payload)
    value = payload
    if normalized:
        value = {
            "v": 5,
            "i": normalized["uid"],
            "t": normalized["title"],
            "n": [
                [
                    node["id"],
                    node["label"],
                    node["shape"],
                    node["tone"],
                    node["x"],
                    node["y"],
                    node["width"],
                    node["height"],
                    node["href"],
                    node["font_size"],
                    node["label_offset_x"],
                    node["label_offset_y"],
                ]
                for node in normalized["nodes"]
            ],
            "e": [
                [
                    edge["from"],
                    edge["to"],
                    edge["label"],
                    edge["style"],
                    edge["description"],
                    edge["route"],
                    edge["bend"],
                ]
                for edge in normalized["edges"]
            ],
            "a": [
                [
                    arrow["id"],
                    arrow["start_x"],
                    arrow["start_y"],
                    arrow["end_x"],
                    arrow["end_y"],
                    arrow["label"],
                    arrow["style"],
                    arrow["description"],
                    arrow["route"],
                    arrow["bend"],
                    arrow["start_anchor"],
                    arrow["end_anchor"],
                ]
                for arrow in normalized["arrows"]
            ],
            "g": [
                [group["id"], group["label"], group["tone"], group["node_ids"]]
                for group in normalized["groups"]
            ],
            "r": [
                [
                    region["id"],
                    region["label"],
                    region["operation"],
                    region["tone"],
                    region["node_ids"],
                    region["label_offset_x"],
                    region["label_offset_y"],
                ]
                for region in normalized["regions"]
            ],
        }
    raw = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


@lru_cache(maxsize=256)
def decode_diagram_payload(encoded):
    if not encoded or len(encoded) > 64000:
        return None

    try:
        padding = "=" * (-len(encoded) % 4)
        payload = json.loads(base64.urlsafe_b64decode(encoded + padding).decode("utf-8"))
    except (binascii.Error, ValueError, UnicodeDecodeError, json.JSONDecodeError):
        return None

    if isinstance(payload, dict) and isinstance(payload.get("n"), list):
        payload = {
            "version": payload.get("v", 2),
            "uid": payload.get("i", ""),
            "title": payload.get("t", "Diyagram"),
            "nodes": [
                {
                    "id": node[0],
                    "label": node[1],
                    "shape": node[2],
                    "tone": node[3],
                    "x": node[4],
                    "y": node[5],
                    "width": node[6] if len(node) > 6 else 152,
                    "height": node[7] if len(node) > 7 else (104 if node[2] == "decision" else 68),
                    "href": node[8] if len(node) > 8 else "",
                    "font_size": node[9] if len(node) > 9 else 15,
                    "label_offset_x": node[10] if len(node) > 10 else 0,
                    "label_offset_y": node[11] if len(node) > 11 else 0,
                }
                for node in payload["n"]
                if isinstance(node, list) and len(node) >= 6
            ],
            "edges": [
                {
                    "from": edge[0],
                    "to": edge[1],
                    "label": edge[2],
                    "style": edge[3],
                    "description": edge[4] if len(edge) > 4 else "",
                    "route": edge[5] if len(edge) > 5 else "auto",
                    "bend": edge[6] if len(edge) > 6 else 0,
                }
                for edge in payload.get("e", [])
                if isinstance(edge, list) and len(edge) >= 4
            ],
            "arrows": [
                {
                    "id": arrow[0],
                    "start_x": arrow[1],
                    "start_y": arrow[2],
                    "end_x": arrow[3],
                    "end_y": arrow[4],
                    "label": arrow[5] if len(arrow) > 5 else "",
                    "style": arrow[6] if len(arrow) > 6 else "solid",
                    "description": arrow[7] if len(arrow) > 7 else "",
                    "route": arrow[8] if len(arrow) > 8 else "straight",
                    "bend": arrow[9] if len(arrow) > 9 else 0,
                    "start_anchor": arrow[10] if len(arrow) > 10 else "",
                    "end_anchor": arrow[11] if len(arrow) > 11 else "",
                }
                for arrow in payload.get("a", [])
                if isinstance(arrow, list) and len(arrow) >= 5
            ],
            "groups": [
                {
                    "id": group[0],
                    "label": group[1],
                    "tone": group[2],
                    "node_ids": group[3],
                }
                for group in payload.get("g", [])
                if isinstance(group, list) and len(group) >= 4
            ],
            "regions": [
                {
                    "id": region[0],
                    "label": region[1],
                    "operation": region[2],
                    "tone": region[3],
                    "node_ids": region[4],
                    "label_offset_x": region[5] if len(region) > 5 else 0,
                    "label_offset_y": region[6] if len(region) > 6 else 0,
                }
                for region in payload.get("r", [])
                if isinstance(region, list) and len(region) >= 5
            ],
        }

    return normalize_diagram_payload(payload)


def normalize_diagram_payload(payload):
    if not isinstance(payload, dict):
        return None

    raw_nodes = payload.get("nodes")
    raw_edges = payload.get("edges")
    raw_arrows = payload.get("arrows", [])
    raw_groups = payload.get("groups", [])
    raw_regions = payload.get("regions", [])
    if (
        not isinstance(raw_nodes, list)
        or not isinstance(raw_edges, list)
        or not isinstance(raw_arrows, list)
        or not isinstance(raw_groups, list)
        or not isinstance(raw_regions, list)
    ):
        return None
    if (
        (not raw_nodes and not raw_arrows)
        or len(raw_nodes) > MAX_NODES
        or len(raw_edges) > MAX_EDGES
        or len(raw_arrows) > MAX_FREE_ARROWS
        or len(raw_groups) > MAX_GROUPS
        or len(raw_regions) > MAX_REGIONS
    ):
        return None

    nodes = []
    node_ids = set()
    for raw_node in raw_nodes:
        if not isinstance(raw_node, dict):
            return None

        node_id = str(raw_node.get("id", ""))[:32]
        if not node_id or not node_id.replace("-", "").replace("_", "").isalnum():
            return None
        if node_id in node_ids:
            return None

        try:
            x = float(raw_node.get("x"))
            y = float(raw_node.get("y"))
            width = float(raw_node.get("width", 152))
            height = float(
                raw_node.get("height", 104 if raw_node.get("shape") == "decision" else 68)
            )
            font_size = float(raw_node.get("font_size", raw_node.get("fontSize", 15)))
            label_offset_x = float(
                raw_node.get("label_offset_x", raw_node.get("labelOffsetX", 0))
            )
            label_offset_y = float(
                raw_node.get("label_offset_y", raw_node.get("labelOffsetY", 0))
            )
        except (TypeError, ValueError):
            return None
        if not all(
            math.isfinite(value)
            for value in (x, y, width, height, font_size, label_offset_x, label_offset_y)
        ):
            return None

        shape = str(raw_node.get("shape", "process"))
        if shape not in ALLOWED_SHAPES:
            shape = "process"

        tone = str(raw_node.get("tone", "neutral"))
        if tone not in ALLOWED_TONES:
            tone = "neutral"

        width = round(min(max(width, MIN_NODE_WIDTH), MAX_NODE_WIDTH), 1)
        height = round(min(max(height, MIN_NODE_HEIGHT), MAX_NODE_HEIGHT), 1)
        half_width = width / 2
        half_height = height / 2
        fallback_label = "" if shape == "set" else "Bölge etiketi" if shape == "label" else "Adım"
        label = " ".join(str(raw_node.get("label", fallback_label)).split())[:240]
        if not label:
            label = fallback_label
        node = {
            "id": node_id,
            "label": label,
            "shape": shape,
            "tone": tone,
            "x": round(min(max(x, half_width + 8), CANVAS_WIDTH - half_width - 8), 1),
            "y": round(min(max(y, half_height + 8), CANVAS_HEIGHT - half_height - 8), 1),
            "width": width,
            "height": height,
            "href": _safe_href(raw_node.get("href", "")),
            "font_size": round(min(max(font_size, MIN_FONT_SIZE), MAX_FONT_SIZE), 1),
        }
        label_offset_x, label_offset_y = _constrain_label_offset(
            node,
            label_offset_x,
            label_offset_y,
        )
        node["label_offset_x"] = label_offset_x
        node["label_offset_y"] = label_offset_y
        nodes.append(node)
        node_ids.add(node_id)

    edges = []
    edge_pairs = set()
    for raw_edge in raw_edges:
        if not isinstance(raw_edge, dict):
            continue
        source = str(raw_edge.get("from", ""))[:32]
        target = str(raw_edge.get("to", ""))[:32]
        pair = (source, target)
        if source not in node_ids or target not in node_ids or pair in edge_pairs:
            continue
        label = " ".join(str(raw_edge.get("label", "")).split())[:50]
        style = str(raw_edge.get("style", "solid"))
        if style not in ALLOWED_EDGE_STYLES:
            style = "solid"
        route = str(raw_edge.get("route", "auto"))
        if route not in ALLOWED_EDGE_ROUTES:
            route = "auto"
        try:
            bend = float(raw_edge.get("bend", 0))
        except (TypeError, ValueError):
            bend = 0
        if not math.isfinite(bend):
            bend = 0
        raw_description = str(raw_edge.get("description", "")).replace("\r\n", "\n")
        raw_description = raw_description.replace("\r", "\n").strip()[:600]
        edges.append(
            {
                "from": source,
                "to": target,
                "label": label,
                "style": style,
                "description": raw_description,
                "route": route,
                "bend": round(min(max(bend, -MAX_EDGE_BEND), MAX_EDGE_BEND), 1),
            }
        )
        edge_pairs.add(pair)

    arrows = []
    arrow_ids = set()
    for index, raw_arrow in enumerate(raw_arrows[:MAX_FREE_ARROWS]):
        if not isinstance(raw_arrow, dict):
            continue
        arrow_id = str(raw_arrow.get("id", f"a{index + 1}"))[:32]
        if (
            not arrow_id
            or arrow_id in arrow_ids
            or not arrow_id.replace("-", "").replace("_", "").isalnum()
        ):
            continue
        try:
            start_x = float(raw_arrow.get("start_x", raw_arrow.get("startX")))
            start_y = float(raw_arrow.get("start_y", raw_arrow.get("startY")))
            end_x = float(raw_arrow.get("end_x", raw_arrow.get("endX")))
            end_y = float(raw_arrow.get("end_y", raw_arrow.get("endY")))
            bend = float(raw_arrow.get("bend", 0))
        except (TypeError, ValueError):
            continue
        if not all(math.isfinite(value) for value in (start_x, start_y, end_x, end_y, bend)):
            continue
        style = str(raw_arrow.get("style", "solid"))
        if style not in ALLOWED_EDGE_STYLES:
            style = "solid"
        route = str(raw_arrow.get("route", "straight"))
        if route not in ALLOWED_EDGE_ROUTES:
            route = "straight"
        description = str(raw_arrow.get("description", "")).replace("\r\n", "\n")
        description = description.replace("\r", "\n").strip()[:600]
        arrows.append(
            {
                "id": arrow_id,
                "start_x": round(min(max(start_x, 8), CANVAS_WIDTH - 8), 1),
                "start_y": round(min(max(start_y, 8), CANVAS_HEIGHT - 8), 1),
                "end_x": round(min(max(end_x, 8), CANVAS_WIDTH - 8), 1),
                "end_y": round(min(max(end_y, 8), CANVAS_HEIGHT - 8), 1),
                "label": " ".join(str(raw_arrow.get("label", "")).split())[:50],
                "style": style,
                "description": description,
                "route": route,
                "bend": round(min(max(bend, -MAX_EDGE_BEND), MAX_EDGE_BEND), 1),
                "start_anchor": str(
                    raw_arrow.get("start_anchor", raw_arrow.get("startAnchor", ""))
                )[:35],
                "end_anchor": str(
                    raw_arrow.get("end_anchor", raw_arrow.get("endAnchor", ""))
                )[:35],
            }
        )
        arrow_ids.add(arrow_id)

    groups = []
    grouped_node_ids = set()
    group_ids = set()
    for index, raw_group in enumerate(raw_groups[:MAX_GROUPS]):
        if not isinstance(raw_group, dict):
            continue
        group_id = str(raw_group.get("id", f"g{index + 1}"))[:32]
        if (
            not group_id
            or group_id in group_ids
            or not group_id.replace("-", "").replace("_", "").isalnum()
        ):
            continue
        raw_member_ids = raw_group.get("node_ids", [])
        if not isinstance(raw_member_ids, list):
            continue
        member_ids = []
        for node_id in raw_member_ids:
            node_id = str(node_id)[:32]
            if node_id in node_ids and node_id not in grouped_node_ids:
                member_ids.append(node_id)
                grouped_node_ids.add(node_id)
        if len(member_ids) < 2:
            grouped_node_ids.difference_update(member_ids)
            continue
        tone = str(raw_group.get("tone", "neutral"))
        if tone not in ALLOWED_TONES:
            tone = "neutral"
        groups.append(
            {
                "id": group_id,
                "label": " ".join(str(raw_group.get("label", "Grup")).split())[:80] or "Grup",
                "tone": tone,
                "node_ids": member_ids,
            }
        )
        group_ids.add(group_id)

    regions = []
    region_ids = set()
    for index, raw_region in enumerate(raw_regions[:MAX_REGIONS]):
        if not isinstance(raw_region, dict):
            continue
        region_id = str(raw_region.get("id", f"r{index + 1}"))[:32]
        if (
            not region_id
            or region_id in region_ids
            or not region_id.replace("-", "").replace("_", "").isalnum()
        ):
            continue
        raw_member_ids = raw_region.get("node_ids", raw_region.get("nodeIds", []))
        if not isinstance(raw_member_ids, list):
            continue
        member_ids = []
        for node_id in raw_member_ids:
            node_id = str(node_id)[:32]
            if node_id in node_ids and node_id not in member_ids:
                member_ids.append(node_id)
        if len(member_ids) < 2:
            continue
        operation = str(raw_region.get("operation", "intersection"))
        if operation not in ALLOWED_REGION_OPERATIONS:
            operation = "intersection"
        tone = str(raw_region.get("tone", "gold"))
        if tone not in ALLOWED_TONES:
            tone = "gold"
        try:
            label_offset_x = float(
                raw_region.get("label_offset_x", raw_region.get("labelOffsetX", 0))
            )
            label_offset_y = float(
                raw_region.get("label_offset_y", raw_region.get("labelOffsetY", 0))
            )
        except (TypeError, ValueError):
            label_offset_x = 0
            label_offset_y = 0
        if not math.isfinite(label_offset_x):
            label_offset_x = 0
        if not math.isfinite(label_offset_y):
            label_offset_y = 0
        label_offset_x = min(CANVAS_WIDTH, max(-CANVAS_WIDTH, label_offset_x))
        label_offset_y = min(CANVAS_HEIGHT, max(-CANVAS_HEIGHT, label_offset_y))
        regions.append(
            {
                "id": region_id,
                "label": " ".join(str(raw_region.get("label", "")).split())[:80],
                "operation": operation,
                "tone": tone,
                "node_ids": member_ids,
                "label_offset_x": label_offset_x,
                "label_offset_y": label_offset_y,
            }
        )
        region_ids.add(region_id)

    valid_anchors = {
        *(f"n:{node_id}" for node_id in node_ids),
        *(f"r:{region_id}" for region_id in region_ids),
    }
    for arrow in arrows:
        if arrow["start_anchor"] not in valid_anchors:
            arrow["start_anchor"] = ""
        if arrow["end_anchor"] not in valid_anchors:
            arrow["end_anchor"] = ""

    uid = str(payload.get("uid", ""))[:32]
    if uid and not uid.replace("-", "").replace("_", "").isalnum():
        uid = ""
    title = " ".join(str(payload.get("title", "Diyagram")).split())[:80] or "Diyagram"
    return {
        "version": 5,
        "uid": uid,
        "title": title,
        "nodes": nodes,
        "edges": edges,
        "arrows": arrows,
        "groups": groups,
        "regions": regions,
    }


def _safe_href(value):
    href = str(value or "").strip()[:500]
    if not href:
        return ""
    if href.startswith("/") and not href.startswith("//"):
        return href
    parsed = urlsplit(href)
    if parsed.scheme in {"http", "https"} and parsed.netloc:
        return href
    return ""


def _node_boundary(node, target, reverse=False):
    dx = target[0] - node["x"]
    dy = target[1] - node["y"]
    if reverse:
        dx *= -1
        dy *= -1
    if not dx and not dy:
        return node["x"], node["y"]

    half_width = node["width"] / 2
    half_height = node["height"] / 2
    if node["shape"] == "set":
        denominator = math.sqrt((dx / half_width) ** 2 + (dy / half_height) ** 2)
        scale = 1 / denominator if denominator else 0
        return node["x"] + (dx * scale), node["y"] + (dy * scale)
    if node["shape"] == "decision":
        denominator = (abs(dx) / half_width) + (abs(dy) / half_height)
        scale = 1 / denominator if denominator else 0
        return node["x"] + (dx * scale), node["y"] + (dy * scale)
    scale_x = half_width / abs(dx) if dx else float("inf")
    scale_y = half_height / abs(dy) if dy else float("inf")
    scale = min(scale_x, scale_y)
    return node["x"] + (dx * scale), node["y"] + (dy * scale)


def _line_crosses_node(start, end, node):
    half_width = (node["width"] / 2) + 18
    half_height = (node["height"] / 2) + 18
    for step in range(1, 20):
        ratio = step / 20
        x = start[0] + ((end[0] - start[0]) * ratio)
        y = start[1] + ((end[1] - start[1]) * ratio)
        if abs(x - node["x"]) <= half_width and abs(y - node["y"]) <= half_height:
            return True
    return False


def _connector_geometry(start, end, route="straight", bend=0, reverse_bend=False, explicit_curve=False):
    resolved_route = "straight" if route == "auto" else route
    if resolved_route == "straight":
        return {
            "path": f"M {start[0]:.1f} {start[1]:.1f} L {end[0]:.1f} {end[1]:.1f}",
            "label_x": (start[0] + end[0]) / 2,
            "label_y": (start[1] + end[1]) / 2 - 10,
        }

    if resolved_route == "orthogonal":
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        if abs(dx) >= abs(dy):
            middle = ((start[0] + end[0]) / 2) + bend
            path = (
                f"M {start[0]:.1f} {start[1]:.1f} H {middle:.1f} "
                f"V {end[1]:.1f} H {end[0]:.1f}"
            )
            label_x = middle
            label_y = ((start[1] + end[1]) / 2) - 10
        else:
            middle = ((start[1] + end[1]) / 2) + bend
            path = (
                f"M {start[0]:.1f} {start[1]:.1f} V {middle:.1f} "
                f"H {end[0]:.1f} V {end[1]:.1f}"
            )
            label_x = ((start[0] + end[0]) / 2)
            label_y = middle - 10
        return {"path": path, "label_x": label_x, "label_y": label_y}

    midpoint_x = (start[0] + end[0]) / 2
    midpoint_y = (start[1] + end[1]) / 2
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = max(math.hypot(dx, dy), 1)
    curve_bend = bend if bend or explicit_curve else (-48 if reverse_bend else 48)
    control_x = midpoint_x + (-dy / length * curve_bend)
    control_y = midpoint_y + (dx / length * curve_bend)
    return {
        "path": (
            f"M {start[0]:.1f} {start[1]:.1f} "
            f"Q {control_x:.1f} {control_y:.1f} {end[0]:.1f} {end[1]:.1f}"
        ),
        "label_x": (start[0] + (2 * control_x) + end[0]) / 4,
        "label_y": (start[1] + (2 * control_y) + end[1]) / 4 - 8,
    }


def _edge_geometry(
    source,
    target,
    all_nodes=None,
    route="auto",
    bend=0,
    has_reverse=False,
    reverse_bend=False,
):
    if source["id"] == target["id"]:
        x = source["x"]
        y = source["y"]
        half_width = source["width"] / 2
        half_height = source["height"] / 2
        return {
            "path": (
                f"M {x + (half_width * .58):.1f} {y - (half_height * .85):.1f} "
                f"C {x + half_width + 60:.1f} {y - half_height - 62:.1f}, "
                f"{x - half_width - 60:.1f} {y - half_height - 62:.1f}, "
                f"{x - (half_width * .58):.1f} {y - (half_height * .85):.1f}"
            ),
            "label_x": x,
            "label_y": y - half_height - 70,
        }

    start = _node_boundary(source, (target["x"], target["y"]))
    end = _node_boundary(target, (source["x"], source["y"]))
    resolved_route = route
    if route == "auto":
        blockers = [
            node
            for node in (all_nodes or [])
            if node["id"] not in {source["id"], target["id"]}
            and _line_crosses_node(start, end, node)
        ]
        resolved_route = "orthogonal" if blockers else "straight"
    if has_reverse and resolved_route == "straight":
        resolved_route = "curve"
    return _connector_geometry(
        start,
        end,
        route=resolved_route,
        bend=bend,
        reverse_bend=reverse_bend,
        explicit_curve=route == "curve",
    )


def _region_interior_points(region, members, bounds, steps=10):
    candidates = [(node["x"], node["y"]) for node in members]
    candidates.extend(
        (
            bounds["left"] + ((bounds["right"] - bounds["left"]) * (column / steps)),
            bounds["top"] + ((bounds["bottom"] - bounds["top"]) * (row / steps)),
        )
        for row in range(steps + 1)
        for column in range(steps + 1)
    )
    return [point for point in candidates if _point_inside_region(point, region, members)]


def _region_anchor_point(region, members, bounds, target=None):
    reference = target or (
        (bounds["left"] + bounds["right"]) / 2,
        (bounds["top"] + bounds["bottom"]) / 2,
    )
    candidates = _region_interior_points(region, members, bounds)
    if not candidates:
        return None
    return min(
        candidates,
        key=lambda point: math.hypot(point[0] - reference[0], point[1] - reference[1]),
    )


def _resolve_arrow_anchor(anchor, nodes_by_id, regions_by_id):
    anchor = str(anchor or "")
    if anchor.startswith("n:"):
        node = nodes_by_id.get(anchor[2:])
        if node:
            return {"type": "node", "node": node, "center": (node["x"], node["y"])}
    if anchor.startswith("r:"):
        region = regions_by_id.get(anchor[2:])
        if region:
            members = [
                nodes_by_id[node_id]
                for node_id in region["node_ids"]
                if node_id in nodes_by_id
            ]
            bounds = _region_bounds(region, members)
            if bounds:
                center = _region_anchor_point(region, members, bounds)
                if not center:
                    return None
                return {
                    "type": "region",
                    "region": region,
                    "members": members,
                    "bounds": bounds,
                    "center": center,
                }
    return None


def _resolved_free_arrow_endpoints(arrow, nodes_by_id=None, regions_by_id=None):
    nodes_by_id = nodes_by_id or {}
    regions_by_id = regions_by_id or {}
    raw_start = (arrow["start_x"], arrow["start_y"])
    raw_end = (arrow["end_x"], arrow["end_y"])
    start_anchor = _resolve_arrow_anchor(arrow.get("start_anchor"), nodes_by_id, regions_by_id)
    end_anchor = _resolve_arrow_anchor(arrow.get("end_anchor"), nodes_by_id, regions_by_id)
    start = start_anchor["center"] if start_anchor else raw_start
    end = raw_end
    if end_anchor and end_anchor["type"] == "node":
        end = _node_boundary(end_anchor["node"], start)
    elif end_anchor and end_anchor["type"] == "region":
        end = _region_anchor_point(
            end_anchor["region"],
            end_anchor["members"],
            end_anchor["bounds"],
            target=start,
        ) or end_anchor["center"]
    return start, end


def _free_arrow_geometry(arrow, nodes_by_id=None, regions_by_id=None):
    start, end = _resolved_free_arrow_endpoints(arrow, nodes_by_id, regions_by_id)
    return _connector_geometry(
        start,
        end,
        route=arrow["route"],
        bend=arrow["bend"],
        explicit_curve=arrow["route"] == "curve",
    )


def _label_lines(node):
    label = node["label"]
    if not label:
        return [], node["font_size"] * 1.22
    font_size = node["font_size"]
    line_height = font_size * 1.22
    line_width = max(5, int((node["width"] - 28) / (font_size * .52)))
    max_lines = max(1, min(20, int((node["height"] - 18) / line_height)))
    lines = wrap(
        label,
        width=line_width,
        break_long_words=True,
        break_on_hyphens=False,
    )[:max_lines]
    if len(lines) == max_lines and " ".join(lines) != label:
        lines[-1] = lines[-1][: max(8, line_width - 3)].rstrip() + "..."
    return lines, line_height


def _constrain_label_offset(node, raw_x, raw_y):
    lines, line_height = _label_lines(node)
    longest_line = max((len(line) for line in lines), default=0)
    text_width = min(max(0, node["width"] - 18), longest_line * node["font_size"] * .56)
    text_height = len(lines) * line_height
    radius_x = max(0, (node["width"] / 2) - (text_width / 2) - 8)
    radius_y = max(0, (node["height"] / 2) - (text_height / 2) - 7)
    x = min(max(float(raw_x), -radius_x), radius_x)
    y = min(max(float(raw_y), -radius_y), radius_y)
    if node["shape"] == "set" and radius_x > 0 and radius_y > 0:
        distance = math.sqrt((x / radius_x) ** 2 + (y / radius_y) ** 2)
        if distance > 1:
            x /= distance
            y /= distance
    elif node["shape"] == "decision" and radius_x > 0 and radius_y > 0:
        distance = abs(x) / radius_x + abs(y) / radius_y
        if distance > 1:
            x /= distance
            y /= distance
    return round(x, 1), round(y, 1)


def _edge_label_width(label):
    return max(48, min(220, (len(label) * 7.4) + 24))


def _node_shape_html(node, attributes=""):
    x = node["x"]
    y = node["y"]
    width = node["width"]
    height = node["height"]
    half_width = width / 2
    half_height = height / 2
    shape = node["shape"]
    if shape == "label":
        return (
            f'<rect x="{x - half_width:.1f}" y="{y - half_height:.1f}" '
            f'width="{width:.1f}" height="{height:.1f}" rx="6" {attributes}/>'
        )
    elif shape == "decision":
        return (
            f'<polygon points="{x:.1f},{y - half_height:.1f} {x + half_width:.1f},{y:.1f} '
            f'{x:.1f},{y + half_height:.1f} {x - half_width:.1f},{y:.1f}" {attributes}/>'
        )
    elif shape == "terminal":
        return (
            f'<rect x="{x - half_width:.1f}" y="{y - half_height:.1f}" '
            f'width="{width:.1f}" height="{height:.1f}" rx="{min(half_height, 34):.1f}" {attributes}/>'
        )
    elif shape == "data":
        inset = min(18, width * .1)
        return (
            f'<polygon points="{x - half_width + inset:.1f},{y - half_height:.1f} '
            f'{x + half_width:.1f},{y - half_height:.1f} '
            f'{x + half_width - inset:.1f},{y + half_height:.1f} '
            f'{x - half_width:.1f},{y + half_height:.1f}" {attributes}/>'
        )
    elif shape == "document":
        return (
            f'<path d="M {x - half_width:.1f} {y - half_height:.1f} '
            f'H {x + half_width:.1f} V {y + half_height - 12:.1f} '
            f'C {x + (half_width * .5):.1f} {y + half_height - 26:.1f}, '
            f'{x + (half_width * .16):.1f} {y + half_height + 8:.1f}, '
            f'{x - (half_width * .26):.1f} {y + half_height - 8:.1f} '
            f'C {x - (half_width * .6):.1f} {y + half_height - 20:.1f}, '
            f'{x - (half_width * .8):.1f} {y + half_height:.1f}, '
            f'{x - half_width:.1f} {y + half_height - 6:.1f} Z" {attributes}/>'
        )
    elif shape == "pyramid":
        inset = width * .18
        return (
            f'<polygon points="{x - half_width + inset:.1f},{y - half_height:.1f} '
            f'{x + half_width - inset:.1f},{y - half_height:.1f} '
            f'{x + half_width:.1f},{y + half_height:.1f} '
            f'{x - half_width:.1f},{y + half_height:.1f}" {attributes}/>'
        )
    elif shape == "set":
        return (
            f'<ellipse cx="{x:.1f}" cy="{y:.1f}" '
            f'rx="{half_width:.1f}" ry="{half_height:.1f}" {attributes}/>'
        )
    return (
        f'<rect x="{x - half_width:.1f}" y="{y - half_height:.1f}" '
        f'width="{width:.1f}" height="{height:.1f}" rx="8" {attributes}/>'
    )


def _render_node(node):
    x = node["x"]
    y = node["y"]
    label_x = x + node["label_offset_x"]
    label_y = y + node["label_offset_y"]
    half_width = node["width"] / 2
    half_height = node["height"] / 2
    shape = node["shape"]
    shape_html = _node_shape_html(node)

    lines, line_height = _label_lines(node)
    first_y = label_y - ((len(lines) - 1) * line_height / 2)
    text_html = "".join(
        f'<tspan x="{label_x:.1f}" y="{first_y + (index * line_height):.1f}">{escape(line)}</tspan>'
        for index, line in enumerate(lines)
    )
    href = escape(node["href"])
    link_class = " answer-diagram-node-linked" if href else ""
    link_data = (
        f' data-diagram-link="{href}" tabindex="0" role="link" '
        f'aria-label="{escape(node["label"] or "Bağlantılı öğe")} bağlantısını aç"'
        if href
        else ""
    )
    link_indicator = (
        f'<text class="answer-diagram-node-link-indicator" '
        f'x="{x + half_width - 15:.1f}" y="{y - half_height + 20:.1f}" '
        'aria-hidden="true">↗</text>'
        if href
        else ""
    )
    return (
        f'<g class="answer-diagram-node answer-diagram-node-{shape} '
        f'answer-diagram-tone-{node["tone"]}{link_class}"{link_data}>'
        f'{shape_html}<text style="font-size:{node["font_size"]:.1f}px">{text_html}</text>{link_indicator}</g>'
    )


def _render_groups(groups, nodes_by_id):
    rendered = []
    for group in groups:
        members = [nodes_by_id[node_id] for node_id in group["node_ids"] if node_id in nodes_by_id]
        if len(members) < 2:
            continue
        left = min(node["x"] - (node["width"] / 2) for node in members) - 26
        top = min(node["y"] - (node["height"] / 2) for node in members) - 42
        right = max(node["x"] + (node["width"] / 2) for node in members) + 26
        bottom = max(node["y"] + (node["height"] / 2) for node in members) + 26
        rendered.append(
            f'<g class="answer-diagram-group answer-diagram-group-{group["tone"]}">'
            f'<rect x="{left:.1f}" y="{top:.1f}" width="{right - left:.1f}" '
            f'height="{bottom - top:.1f}" rx="14" />'
            f'<text x="{left + 16:.1f}" y="{top + 25:.1f}">{escape(group["label"])}</text>'
            '</g>'
        )
    return "".join(rendered)


def _region_symbol(operation):
    if operation == "union":
        return "∪"
    if operation == "difference":
        return "∖"
    return "∩"


def _point_inside_node(point, node):
    half_width = node["width"] / 2
    half_height = node["height"] / 2
    dx = point[0] - node["x"]
    dy = point[1] - node["y"]
    if node["shape"] == "set":
        return (dx / half_width) ** 2 + (dy / half_height) ** 2 <= 1
    if node["shape"] == "decision":
        return abs(dx) / half_width + abs(dy) / half_height <= 1
    return abs(dx) <= half_width and abs(dy) <= half_height


def _point_inside_region(point, region, members):
    if len(members) < 2:
        return False
    membership = [_point_inside_node(point, node) for node in members]
    if region["operation"] == "union":
        return any(membership)
    if region["operation"] == "difference":
        return membership[0] and not any(membership[1:])
    return all(membership)


def _intersection_has_visible_area(bounds, members):
    candidates = [(node["x"], node["y"]) for node in members]
    steps = 8
    candidates.extend(
        (
            bounds["left"] + ((bounds["right"] - bounds["left"]) * (column / steps)),
            bounds["top"] + ((bounds["bottom"] - bounds["top"]) * (row / steps)),
        )
        for row in range(steps + 1)
        for column in range(steps + 1)
    )
    return any(all(_point_inside_node(point, node) for node in members) for point in candidates)


def _region_bounds(region, members):
    if not members:
        return None
    bounds = [
        {
            "left": node["x"] - (node["width"] / 2),
            "top": node["y"] - (node["height"] / 2),
            "right": node["x"] + (node["width"] / 2),
            "bottom": node["y"] + (node["height"] / 2),
        }
        for node in members
    ]
    if region["operation"] == "intersection":
        intersection = {
            "left": max(item["left"] for item in bounds),
            "top": max(item["top"] for item in bounds),
            "right": min(item["right"] for item in bounds),
            "bottom": min(item["bottom"] for item in bounds),
        }
        if (
            intersection["right"] > intersection["left"]
            and intersection["bottom"] > intersection["top"]
            and _intersection_has_visible_area(intersection, members)
        ):
            return intersection
        return None
    if region["operation"] == "difference":
        return bounds[0]
    return {
        "left": min(item["left"] for item in bounds),
        "top": min(item["top"] for item in bounds),
        "right": max(item["right"] for item in bounds),
        "bottom": max(item["bottom"] for item in bounds),
    }


def _render_regions(regions, nodes_by_id, digest):
    definitions = []
    rendered = []
    pattern_ids = {}
    for tone in sorted(ALLOWED_TONES):
        pattern_id = f"diagram-region-pattern-{digest}-{tone}"
        pattern_ids[tone] = pattern_id
        definitions.append(
            f'<pattern id="{pattern_id}" width="12" height="12" '
            'patternUnits="userSpaceOnUse" patternTransform="rotate(36)">'
            f'<line x1="0" y1="0" x2="0" y2="12" '
            f'class="answer-diagram-region-hatch answer-diagram-region-hatch-{tone}" />'
            '</pattern>'
        )

    for region in regions:
        members = [nodes_by_id[node_id] for node_id in region["node_ids"] if node_id in nodes_by_id]
        if len(members) < 2:
            continue
        bounds = _region_bounds(region, members)
        if bounds is None:
            continue
        pattern_id = pattern_ids[region["tone"]]
        shape_attributes = (
            f'class="answer-diagram-region-shape" fill="url(#{pattern_id})" '
            'stroke="none" pointer-events="none" '
        )
        if region["operation"] == "union":
            visual = "".join(_node_shape_html(node, shape_attributes) for node in members)
        elif region["operation"] == "difference":
            mask_id = f'diagram-region-mask-{digest}-{region["id"]}'
            mask_shapes = [
                f'<rect x="0" y="0" width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}" fill="black" />',
                _node_shape_html(members[0], 'fill="white" stroke="none" '),
            ]
            mask_shapes.extend(
                _node_shape_html(node, 'fill="black" stroke="none" ')
                for node in members[1:]
            )
            definitions.append(
                f'<mask id="{mask_id}" maskUnits="userSpaceOnUse" x="0" y="0" '
                f'width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}">'
                f'{"".join(mask_shapes)}</mask>'
            )
            first = members[0]
            visual = (
                f'<rect x="{first["x"] - (first["width"] / 2):.1f}" '
                f'y="{first["y"] - (first["height"] / 2):.1f}" '
                f'width="{first["width"]:.1f}" height="{first["height"]:.1f}" '
                f'class="answer-diagram-region-shape" fill="url(#{pattern_id})" '
                f'mask="url(#{mask_id})" pointer-events="none" />'
            )
        else:
            visual = _node_shape_html(members[0], shape_attributes)
            for index, member in enumerate(members[1:]):
                clip_id = f'diagram-region-clip-{digest}-{region["id"]}-{index}'
                definitions.append(
                    f'<clipPath id="{clip_id}" clipPathUnits="userSpaceOnUse">'
                    f'{_node_shape_html(member)}</clipPath>'
                )
                visual = f'<g clip-path="url(#{clip_id})">{visual}</g>'

        label = region["label"]
        label_html = ""
        if label:
            base_x = (bounds["left"] + bounds["right"]) / 2
            base_y = (
                (bounds["top"] + bounds["bottom"]) / 2
                if region["operation"] == "intersection"
                else bounds["top"] + 24
            )
            label_x = min(
                CANVAS_WIDTH - 12,
                max(12, base_x + region["label_offset_x"]),
            )
            label_y = min(
                CANVAS_HEIGHT - 12,
                max(12, base_y + region["label_offset_y"]),
            )
            label_html = (
                '<g class="answer-diagram-region-label">'
                f'<text x="{label_x:.1f}" y="{label_y + 1:.1f}">{escape(label)}</text>'
                '</g>'
            )
        rendered.append(
            f'<g class="answer-diagram-region answer-diagram-region-{region["operation"]}">'
            f'{visual}{label_html}</g>'
        )
    return "".join(definitions), "".join(rendered)


def _diagram_viewbox(nodes, arrows=None, nodes_by_id=None, regions_by_id=None):
    x_values = []
    y_values = []
    for node in nodes:
        x_values.extend((node["x"] - (node["width"] / 2), node["x"] + (node["width"] / 2)))
        y_values.extend((node["y"] - (node["height"] / 2), node["y"] + (node["height"] / 2)))
    for arrow in arrows or []:
        (start_x, start_y), (end_x, end_y) = _resolved_free_arrow_endpoints(
            arrow,
            nodes_by_id,
            regions_by_id,
        )
        x_values.extend((start_x, end_x))
        y_values.extend((start_y, end_y))
        if arrow["route"] == "orthogonal":
            if abs(end_x - start_x) >= abs(end_y - start_y):
                x_values.append(((start_x + end_x) / 2) + arrow["bend"])
            else:
                y_values.append(((start_y + end_y) / 2) + arrow["bend"])
        elif arrow["route"] == "curve":
            dx = end_x - start_x
            dy = end_y - start_y
            length = max(math.hypot(dx, dy), 1)
            x_values.append(((start_x + end_x) / 2) + (-dy / length * arrow["bend"]))
            y_values.append(((start_y + end_y) / 2) + (dx / length * arrow["bend"]))

    if not x_values or not y_values:
        return 0, 0, VIEWPORT_WIDTH, VIEWPORT_HEIGHT
    left = min(x_values)
    top = min(y_values)
    right = max(x_values)
    bottom = max(y_values)

    if left >= 0 and top >= 0 and right <= VIEWPORT_WIDTH and bottom <= VIEWPORT_HEIGHT:
        return 0, 0, VIEWPORT_WIDTH, VIEWPORT_HEIGHT

    padding = 80
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(CANVAS_WIDTH, right + padding)
    bottom = min(CANVAS_HEIGHT, bottom + padding)

    width = right - left
    height = bottom - top
    if width < VIEWPORT_WIDTH:
        extra = VIEWPORT_WIDTH - width
        left = max(0, left - (extra / 2))
        right = min(CANVAS_WIDTH, left + VIEWPORT_WIDTH)
        left = max(0, right - VIEWPORT_WIDTH)
    if height < VIEWPORT_HEIGHT:
        extra = VIEWPORT_HEIGHT - height
        top = max(0, top - (extra / 2))
        bottom = min(CANVAS_HEIGHT, top + VIEWPORT_HEIGHT)
        top = max(0, bottom - VIEWPORT_HEIGHT)

    return round(left, 1), round(top, 1), round(right - left, 1), round(bottom - top, 1)


def render_diagram_html(payload, encoded_payload):
    normalized = normalize_diagram_payload(payload)
    if not normalized:
        return ""

    digest = hashlib.sha1(encoded_payload.encode("ascii")).hexdigest()[:10]
    arrow_id = f"diagram-arrow-{digest}"
    nodes_by_id = {node["id"]: node for node in normalized["nodes"]}
    regions_by_id = {region["id"]: region for region in normalized["regions"]}
    edge_pairs = {(edge["from"], edge["to"]) for edge in normalized["edges"]}

    edge_html = []
    for edge_index, edge in enumerate(normalized["edges"]):
        source = nodes_by_id[edge["from"]]
        target = nodes_by_id[edge["to"]]
        reverse_pair = (edge["to"], edge["from"])
        has_reverse = reverse_pair in edge_pairs and reverse_pair != (edge["from"], edge["to"])
        geometry = _edge_geometry(
            source,
            target,
            all_nodes=normalized["nodes"],
            route=edge["route"],
            bend=edge["bend"],
            has_reverse=has_reverse,
            reverse_bend=has_reverse and edge["from"] > edge["to"],
        )
        edge_class = "answer-diagram-edge"
        if edge["style"] == "dashed":
            edge_class += " answer-diagram-edge-dashed"
        label_html = ""
        if edge["label"]:
            label_width = _edge_label_width(edge["label"])
            label_html = (
                '<g class="answer-diagram-edge-label-group">'
                f'<rect class="answer-diagram-edge-label-bg" '
                f'x="{geometry["label_x"] - (label_width / 2):.1f}" '
                f'y="{geometry["label_y"] - 18:.1f}" width="{label_width:.1f}" '
                'height="26" rx="13" />'
                f'<text class="answer-diagram-edge-label" '
                f'x="{geometry["label_x"]:.1f}" y="{geometry["label_y"]:.1f}">'
                f'{escape(edge["label"])}</text></g>'
            )
        edge_description = escape(edge["description"])
        edge_label = escape(edge["label"] or "Bağlantı")
        interactive_class = " answer-diagram-edge-interactive" if edge["description"] else ""
        edge_accessibility = (
            f'tabindex="0" role="button" aria-label="{edge_label} açıklamasını aç"'
            if edge["description"]
            else ""
        )
        edge_html.append(
            f'<g class="answer-diagram-edge-group{interactive_class}" '
            f'data-diagram-edge-index="{edge_index}" '
            f'data-diagram-edge-label="{edge_label}" '
            f'data-diagram-edge-description="{edge_description}" '
            f'{edge_accessibility}>'
            f'<path class="{edge_class}" d="{geometry["path"]}" '
            f'marker-end="url(#{arrow_id})" />'
            f'<path class="answer-diagram-edge-hit" d="{geometry["path"]}" />'
            f'{label_html}</g>'
        )

    edge_offset = len(normalized["edges"])
    for arrow_index, arrow in enumerate(normalized["arrows"]):
        geometry = _free_arrow_geometry(arrow, nodes_by_id, regions_by_id)
        edge_class = "answer-diagram-edge"
        if arrow["style"] == "dashed":
            edge_class += " answer-diagram-edge-dashed"
        label_html = ""
        if arrow["label"]:
            label_width = _edge_label_width(arrow["label"])
            label_html = (
                '<g class="answer-diagram-edge-label-group">'
                f'<rect class="answer-diagram-edge-label-bg" '
                f'x="{geometry["label_x"] - (label_width / 2):.1f}" '
                f'y="{geometry["label_y"] - 18:.1f}" width="{label_width:.1f}" '
                'height="26" rx="13" />'
                f'<text class="answer-diagram-edge-label" '
                f'x="{geometry["label_x"]:.1f}" y="{geometry["label_y"]:.1f}">'
                f'{escape(arrow["label"])}</text></g>'
            )
        description = escape(arrow["description"])
        label = escape(arrow["label"] or "Bağımsız ok")
        interactive_class = " answer-diagram-edge-interactive" if arrow["description"] else ""
        accessibility = (
            f'tabindex="0" role="button" aria-label="{label} açıklamasını aç"'
            if arrow["description"]
            else ""
        )
        edge_html.append(
            f'<g class="answer-diagram-edge-group answer-diagram-free-arrow-group{interactive_class}" '
            f'data-diagram-edge-index="{edge_offset + arrow_index}" '
            f'data-diagram-edge-label="{label}" '
            f'data-diagram-edge-description="{description}" '
            f'{accessibility}>'
            f'<path class="{edge_class}" d="{geometry["path"]}" '
            f'marker-end="url(#{arrow_id})" />'
            f'<path class="answer-diagram-edge-hit" d="{geometry["path"]}" />'
            f'{label_html}</g>'
        )

    groups_html = _render_groups(normalized["groups"], nodes_by_id)
    regions_defs, regions_html = _render_regions(normalized["regions"], nodes_by_id, digest)
    layer_priority = {"set": 0, "pyramid": 1, "label": 3}
    ordered_nodes = sorted(
        enumerate(normalized["nodes"]),
        key=lambda item: (layer_priority.get(item[1]["shape"], 2), item[0]),
    )
    nodes_html = "".join(_render_node(node) for _, node in ordered_nodes)
    viewbox = _diagram_viewbox(
        normalized["nodes"],
        normalized["arrows"],
        nodes_by_id,
        regions_by_id,
    )
    title = escape(normalized["title"])
    summary = escape(
        f'{normalized["title"]}: {len(normalized["nodes"])} adım, '
        f'{len(normalized["edges"]) + len(normalized["arrows"])} bağlantı'
    )
    return (
        f'<figure class="answer-diagram" data-diagram-payload="{encoded_payload}" '
        f'data-diagram-title="{title}" data-diagram-id="{escape(normalized["uid"] or digest)}">'
        '<div class="answer-diagram-toolbar">'
        '<button type="button" class="answer-diagram-open" '
        f'aria-label="{title} diyagramını büyüt">'
        f'<i class="bi bi-diagram-3" aria-hidden="true"></i><span>{title}</span>'
        '</button>'
        '<div class="answer-diagram-actions">'
        '<button type="button" class="answer-diagram-toggle" aria-expanded="true" '
        f'aria-label="{title} diyagramını gizle" title="Diyagramı gizle">'
        '<i class="bi bi-chevron-up" aria-hidden="true"></i></button>'
        '<button type="button" class="answer-diagram-expand" '
        f'aria-label="{title} diyagramını büyüt" title="Tam ekranda aç">'
        '<i class="bi bi-arrows-fullscreen" aria-hidden="true"></i></button>'
        '</div></div>'
        '<div class="answer-diagram-body">'
        f'<svg viewBox="{viewbox[0]} {viewbox[1]} {viewbox[2]} {viewbox[3]}" '
        f'role="img" aria-label="{summary}">'
        '<defs>'
        f'<marker id="{arrow_id}" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M 0 0 L 10 5 L 0 10 z" class="answer-diagram-arrow" />'
        '</marker>'
        f'{regions_defs}'
        '</defs>'
        f'<g class="answer-diagram-groups">{groups_html}</g>'
        f'<g class="answer-diagram-edges">{"".join(edge_html)}</g>'
        f'<g class="answer-diagram-nodes">{nodes_html}</g>'
        f'<g class="answer-diagram-regions">{regions_html}</g>'
        '</svg>'
        '</div>'
        f'<figcaption class="visually-hidden">{summary}</figcaption>'
        '</figure>'
    )
