#!/usr/bin/env python3
"""Shared, stdlib-only factual geometry helpers; all original part/vertex ordering retained."""
import hashlib
import json
import math
import re
import sys
from types import SimpleNamespace

sys.dont_write_bytecode = True


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def receipt(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha(data)}


def verified(path, record):
    data = path.read_bytes()
    assert len(data) == record["bytes"] and sha(data) == record["sha256"], path.name
    if "git_blob_sha" in record:
        git_blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert git_blob == record["git_blob_sha"], path.name
    return data


def polygon_parts(geom):
    assert geom["type"] in ("Polygon", "MultiPolygon")
    return [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]


def line_parts(geom):
    assert geom["type"] in ("LineString", "MultiLineString")
    return [geom["coordinates"]] if geom["type"] == "LineString" else geom["coordinates"]


parts = line_parts


def bounds(points):
    assert points
    for point in points:
        assert len(point) == 2 and all(isinstance(v, (int, float)) and math.isfinite(v) for v in point)
        assert -180 <= point[0] <= 180 and -90 <= point[1] <= 90
    return [min(p[0] for p in points), min(p[1] for p in points), max(p[0] for p in points), max(p[1] for p in points)]


def lake_metrics(geom, ordered=False):
    polygons = polygon_parts(geom)
    vertices = [v for polygon in polygons for ring in polygon for v in ring]
    assert all(p and all(len(r) >= 4 and r[0] == r[-1] for r in p) for p in polygons)
    result = {
        "type": geom["type"], "polygon_part_count": len(polygons),
        "ring_counts_by_part": [len(p) for p in polygons],
        "coordinate_counts_by_part_and_ring": [[len(r) for r in p] for p in polygons],
        "total_coordinates_including_closure": len(vertices),
        "bbox": bounds(vertices), "all_rings_closed": True,
        "canonical_geometry_sha256": sha(canonical(geom)),
    }
    if ordered:
        result["ordered_parts"] = [
            {
                "part_index": i,
                "ordered_rings": [
                    {"ring_index": j, "coordinate_count_including_closure": len(r), "ordered_coordinate_sha256": sha(canonical(r))}
                    for j, r in enumerate(polygon)
                ],
                "canonical_part_sha256": sha(canonical(polygon)),
            }
            for i, polygon in enumerate(polygons)
        ]
    return result


def river_metrics(geom):
    segments = line_parts(geom)
    vertices = [v for segment in segments for v in segment]
    assert all(len(segment) >= 2 for segment in segments)
    return {
        "type": geom["type"], "part_count": len(segments),
        "coordinate_counts_by_part": [len(segment) for segment in segments],
        "coordinate_count": len(vertices), "bounds": bounds(vertices),
        "fragment_endpoints": [segments[0][0], segments[-1][-1]],
        "canonical_geometry_sha256": sha(canonical(geom)),
        "coordinate_order": "Exact production decoder part and vertex order; no simplification, sorting, repair or reversal.",
    }


def metrics(geom):
    segments = line_parts(geom)
    vertices = [v for segment in segments for v in segment]
    assert segments and all(len(segment) >= 2 for segment in segments)
    for p in vertices:
        assert len(p) == 2 and all(math.isfinite(v) for v in p) and -180 <= p[0] <= 180 and -90 <= p[1] <= 90
    return {
        "type": geom["type"], "part_count": len(segments), "coordinate_count": len(vertices),
        "coordinate_counts_by_part": [len(segment) for segment in segments],
        "ordered_parts": [
            {"part_index": i, "coordinate_count": len(segment), "ordered_coordinate_sha256": sha(canonical(segment))}
            for i, segment in enumerate(segments)
        ],
        "bounds": [min(p[0] for p in vertices), min(p[1] for p in vertices), max(p[0] for p in vertices), max(p[1] for p in vertices)],
        "fragment_endpoints": [segments[0][0], segments[-1][-1]],
        "canonical_geometry_sha256": sha(canonical(geom)),
        "coordinate_order": "Exact production decoder part and vertex order; no simplification, sorting, repair or reversal.",
    }


def name_fields(metadata):
    return {k: v for k, v in metadata.items() if k == "name" or k.startswith("name_") or k in ("nameKo", "nameEn", "nameOriginal", "mainstemNameKo")}


def terminal_facts(metadata, geom):
    terminal = metadata.get("terminal")
    if not terminal:
        return None
    end = line_parts(geom)[-1][-1]
    quantized = [round(v, 6) for v in terminal["renderEndpoint"]]
    return {
        "class": terminal["class"], "source_endpoint": terminal["sourceEndpoint"],
        "render_endpoint_before_quantization": terminal["renderEndpoint"],
        "render_endpoint_quantized": quantized,
        "source_endpoint_equals_render_endpoint": terminal["sourceEndpoint"] == terminal["renderEndpoint"],
        "decoded_last_vertex_matches_render_endpoint_quantized": end == quantized,
        "meaning": "Source endpoint means the retained baseline metadata value, not a coordinate independently obtained from original HydroRIVERS source geometry.",
    }


def source_features(raw, identifiers):
    text = raw.decode("utf-8")
    decoder = json.JSONDecoder()
    pos = text.index("[", text.index('"features"')) + 1
    found = {}
    index = 0
    while True:
        while text[pos].isspace() or text[pos] == ",":
            pos += 1
        if text[pos] == "]":
            break
        feature, end = decoder.raw_decode(text, pos)
        ident = str(feature["properties"]["source_id"])
        if ident in identifiers:
            assert ident not in found
            found[ident] = (index, feature, text[pos:end].encode("utf-8"))
        index += 1
        pos = end
    assert set(found) == set(identifiers)
    return found


def for_batch(batch):
    """Expose the historical batch's API with only its ordered-lake difference."""
    match = re.search(r"(?:batch-)?r(\d+)$", str(batch))
    if not match:
        raise ValueError("Expected a batch such as batch-r04")
    number = int(match.group(1))
    return SimpleNamespace(
        canonical=canonical, sha=sha, receipt=receipt, verified=verified,
        polygon_parts=polygon_parts, line_parts=line_parts, bounds=bounds,
        lake_metrics=lambda g: lake_metrics(g, ordered=(number != 4)),
        river_metrics=river_metrics, source_features=source_features,
        name_fields=name_fields, parts=parts, metrics=metrics,
        terminal_facts=terminal_facts,
    )
