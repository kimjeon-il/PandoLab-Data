# Shared reconstruction helpers (P1)

The 95 copies of recover-remaining-queue.py, test-remaining-queue.py and geometry-support.py in batch-r04 through batch-r46 were 12 unique Git blobs. They have been replaced by three stdlib-only implementations and version-map.json.

Run from the repository root with a pinned committed inventory and a selected batch index:

```
python3 reports/hydro/names/reconstruction-2026-10-09/shared/recover_remaining_queue.py --batch r22 --inventory PATH/TO/inventory.csv.gz --index reports/hydro/names/reconstruction-2026-10-09/batch-r22/reconstruction-index.json
python3 reports/hydro/names/reconstruction-2026-10-09/shared/test_remaining_queue.py --batch r22 --inventory PATH/TO/inventory.csv.gz --index reports/hydro/names/reconstruction-2026-10-09/batch-r22/reconstruction-index.json
```

Version policy ranges and immutable original Git blob SHAs are listed in version-map.json. Geometry entry points are provided by geometry_support.for_batch("r04") etc.; this preserves the early/later ordered-part receipt distinction.

The historical batch manifests, recorded validation results and SHA pins describe the *original execution at originalRevision*, not a claim that old package validators will replay byte-for-byte after consolidation. To inspect the archived scripts, use that immutable Git commit. Source data and batch research records are unchanged. No network access, packages or new external programs are required by the shared implementations.
