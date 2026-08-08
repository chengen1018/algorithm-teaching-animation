# Lightweight Delivery Check Design

## Decision

Stage 5 keeps one delivery-check flow only. It does not expose release, CI,
strict, or optional validation modes, and it does not dispatch a separate
post-render media-validator agent.

Stage 4 remains the authoritative gate for code correctness, semantic fidelity,
and pre-render layout. Stage 5 only confirms that the approved render produced
usable media artifacts.

## Stage 5 delivery check

After `FINAL_RENDER` has produced the four Scene MP4s, the combined MP4, and a
frozen `render_manifest.md`, the coordinator runs `DELIVERY_CHECK`.

The check has exactly three operations:

1. Run `ffprobe -v error -show_format -show_streams -of json` on all five MP4
   files. A missing or zero-byte file therefore fails through the same probe;
   no separate existence/size check is maintained.
2. Run `ffmpeg -v error -i <combined.mp4> -f null -` to verify the combined
   artifact can be decoded. Individual Scene files are covered by the probes.
3. Recalculate the current `generated_algo_scene.py` SHA-256 and compare it
   with the approved/rendered source hash recorded in the frozen manifest. A
   mismatch returns the workflow to Stage 4 code preparation.

Scene order is established by the four-Scene contract and the render commands;
`DELIVERY_CHECK` does not perform a separate post-render order assertion.

## Evidence and failure routing

The coordinator writes a concise `delivery_check_result.md` containing the
three command groups, exit status, the source hash comparison, and `PASS` or
`FAIL`. The check does not modify source, the manifest, or any MP4.

- Probe or combined-decode failure: remain in Stage 5 `FINAL_RENDER` and
  regenerate the affected output.
- Code hash mismatch: return to Stage 4 `CODE_PREPARATION` and repeat the
  layout/review gates.
- No other post-render semantic or layout review is introduced.

## Rationale

The deterministic pre-render layout and semantic gates prevent expensive
incorrect renders. The remaining Stage 5 checks are intentionally small and
machine-verifiable; they protect against missing, unreadable, or stale output
without spending tokens on a second agent or a verbose five-file audit report.
