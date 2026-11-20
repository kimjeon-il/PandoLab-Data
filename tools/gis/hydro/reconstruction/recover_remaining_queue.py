#!/usr/bin/env python3
"""Offline remaining-queue reconstruction shared by batches r07-r46.

Only the policy for recorded targets, holds and pending material evolves by batch.
No network or automatic application.
"""
import argparse
import collections
import csv
import gzip
import hashlib
import io
import json
import pathlib
import re
import sys

sys.dont_write_bytecode = True
INVENTORY_SHA = "5d1e12b1a6daa695419173dea491ff0c8c5583ed9e28ba517ba4a599bcd589db"
HOLD_BASE = {"whole_polygon_scope_hold", "supported_reservoir_association_geometry_hold", "candidate_waterbody_identity_extent_hold"}
HOLD_COMPOUND = "compound_feature_name_scope_hold"
HOLD_RIVER = "river_group_name_scope_hold"


def batch_number(value):
    if isinstance(value, int):
        number = value
    else:
        match = re.search(r"(?:batch-)?r(\d+)$", str(value))
        if not match:
            raise ValueError("Expected a batch such as r22 or batch-r22")
        number = int(match.group(1))
    if not 7 <= number <= 46:
        raise ValueError("Remaining-queue batches supported: r07-r46")
    return number


def rebuild(inventory_bytes, index, include_ids=False, batch=None):
    b = batch_number(batch)
    assert hashlib.sha256(inventory_bytes).hexdigest() == INVENTORY_SHA, "initial inventory byte hash mismatch"
    rows = list(csv.DictReader(io.StringIO(gzip.decompress(inventory_bytes).decode("utf-8"))))
    assert len(rows) == 5173 and len({r["aw_id"] for r in rows}) == 5173, "initial inventory units"
    eligible = [r for r in rows if r["classification"] != "named_display"]
    assert len(eligible) == 4065, "eligible initial universe"
    eligible_by_id = {r["aw_id"]: r for r in eligible}
    normal = lambda r: "river_group" if r["category"] == "river" else r["category"]
    assert collections.Counter(normal(r) for r in eligible) == {"river_group": 3455, "lake": 610}, "initial type counts"
    records = index["records"]
    reviewed = [r["aw_id"] for r in records]
    assert len(reviewed) == len(set(reviewed)) == index["total_distinct_reconstructed_targets"], "duplicate/count index mismatch"
    assert set(reviewed) <= set(eligible_by_id), "reviewed target is not initially eligible"
    assert all(r["category"] == normal(eligible_by_id[r["aw_id"]]) for r in records), "target type mismatch"
    assert all(r["automatic_application"] is False for r in records), "application not allowed by research index"
    assert index["automatic_application"] is False
    residual = [r for r in eligible if r["aw_id"] not in set(reviewed)]
    by_type = dict(collections.Counter(normal(r) for r in residual))
    facts = index["remaining_queue_recovery"]
    assert facts["initial_inventory"]["sha256"] == INVENTORY_SHA
    assert facts["eligible_universe_count"] == 4065
    assert facts["reviewed_index_targets"] == len(reviewed)
    assert facts["remaining_without_reconstructed_record"] == len(residual)
    assert facts["remaining_without_reconstructed_record_by_type"] == by_type
    assert facts["historical_never_reviewed_count_claimed"] is False

    result = {
        "status": "passed", "initial_inventory_rows": 5173,
        "initial_eligible_targets": 4065, "reviewed_index_targets": len(reviewed),
        "remaining_without_reconstructed_record": len(residual),
        "remaining_by_type": by_type,
    }
    if b >= 11:
        pending = [r["aw_id"] for r in records if r.get("source_access_limited") is True]
        pending_any = pending
        material = []
        if b >= 39:
            material = [r["aw_id"] for r in records if r.get("source_material_pending") is True]
            pending_any = pending + material
            assert not (set(pending) & set(material)), "pending classes overlap"
            assert index["pending_material_ids"] == material and index["pending_material_count"] == len(material), "material-pending index mismatch"
            assert index["pending_any_ids"] == pending_any and index["pending_any_count"] == len(pending_any), "any-pending index mismatch"
            material_classes = {"source_coverage_incomplete"}
            if b >= 45:
                material_classes.add("source_material_insufficient")
            assert all(
                r.get("full_feature_correspondence_review_completed") is False
                and r.get("follow_up_required") is True
                and r.get("source_access_limited") is False
                and r.get("research_category") in material_classes
                for r in records if r["aw_id"] in material
            ), "material-pending coverage falsely completed or relabelled"
        hold_classes = set(HOLD_BASE)
        if b >= 12:
            hold_classes.add(HOLD_COMPOUND)
        if b >= 22:
            hold_classes.add(HOLD_RIVER)
        holds = [r["aw_id"] for r in records if r["research_category"] in hold_classes and r["aw_id"] not in pending_any]
        assert index["recorded_index_targets"] == len(records) and index["complete_identity_review_claimed_for_all_records"] is False
        assert index["pending_access_ids"] == pending and index["pending_access_count"] == len(pending), "pending-access index mismatch"
        assert index["scope_hold_ids"] == holds and index["scope_hold_count"] == len(holds), "scope-hold index mismatch"
        assert not (set(pending_any) & {r["aw_id"] for r in residual}) and not (set(pending_any) & set(holds))
        assert all(
            r.get("full_feature_correspondence_review_completed") is False and r.get("follow_up_required") is True
            for r in records if r["aw_id"] in pending
        ), "access-pending coverage falsely completed"
        result.update({
            "recorded_index_targets": len(records),
            "pending_access_ids": pending, "pending_access_count": len(pending),
        })
        if b >= 39:
            result.update({
                "pending_material_ids": material, "pending_material_count": len(material),
                "pending_any_ids": pending_any, "pending_any_count": len(pending_any),
            })
        result.update({"scope_hold_ids": holds, "scope_hold_count": len(holds)})
    result.update({
        "queue_order": "original_inventory_row_order",
        "scope": "Remaining means absent from this fresh reconstructed index. It does not mean historically never researched; the unavailable historical504-record ledger is not reconstructed.",
        "network_calls": 0, "automatic_application": False,
    })
    if include_ids:
        result["remaining_aw_ids"] = [r["aw_id"] for r in residual]
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", help="r07-r46; inferred from --index parent if omitted")
    parser.add_argument("--inventory", required=True, type=pathlib.Path)
    parser.add_argument("--index", required=True, type=pathlib.Path)
    parser.add_argument("--include-ids", action="store_true")
    args = parser.parse_args()
    batch = args.batch or args.index.parent.name
    output = rebuild(args.inventory.read_bytes(), json.loads(args.index.read_text()), args.include_ids, batch)
    print(json.dumps(output, ensure_ascii=False, indent=2))
