# Rendered Media Validator Contract

## Role boundary

`rendered_media_validator` is the post-render media-validation role. It
validates the four rendered Scene MP4 files and their combined MP4 against the
approved source and gate evidence, render manifest, and narration manifest.
It does not render scenes, modify source, modify manifests, edit media, or
re-encode artifacts.

## Required inputs

Before starting, read every coordinator-provided absolute path in full:

1. `<project-root>/generated_algo_scene.py`
2. `<project-root>/scene_code_review_handoff.md`
3. `<project-root>/scene_review_result.md`
4. `<project-root>/render_manifest.md`
5. `<project-root>/narration_manifest.json`
6. the four Scene MP4 paths, in approved Scene order
7. the combined MP4 path

All input and output paths used in commands and the result must be absolute
paths.

## Preflight

- Every required source, gate, manifest, and media file exists and is readable.
- `scene_review_result.md` is `PASS` and binds the same source SHA-256 as the
  handoff and current `generated_algo_scene.py`.
- `render_manifest.md` lists exactly four non-empty Scene MP4 files in approved
  order and one non-empty combined MP4, all corresponding to the approved
  source.
- `narration_manifest.json` is readable and supplies the expected narration or
  audio timing evidence needed for the duration and audio checks.

If preflight fails, write `rendered_media_validation_result.md` with
`Result: FAIL`, the failed evidence, and every hash that can be calculated.
Do not infer missing media, order, audio, duration, or gate evidence.

## Forbidden actions

- Do not modify `generated_algo_scene.py`, review/gate files, manifests, or
  result inputs.
- Do not run Manim rendering or regenerate any media artifact.
- Do not trim, concatenate, repair, replace, transcode, re-encode, or otherwise
  modify the Scene MP4s or combined MP4.
- Do not hide, truncate, delete, or manually waive failed checks.

## Procedure

1. Record the approved source path and SHA-256, and verify its identity against
   the handoff, review result, and render manifest.
2. For every one of the four Scene MP4s, in manifest order, and then for the
   combined MP4, run and capture complete stdout, stderr, and exit code for:

   ```bash
   ffprobe -v error -show_format -show_streams -of json <file.mp4>
   ffmpeg -v error -i <file.mp4> -f null -
   sha256sum <file.mp4>
   ```

3. Record each file's absolute path, SHA-256, container/stream metadata,
   duration, dimensions, frame rate, codec information, and audio-stream
   presence and metadata from the command output.
4. Compare every Scene MP4's duration and audio evidence with its corresponding
   narration-manifest entry. Confirm that all four Scene files follow the
   approved render-manifest order, and that the combined MP4 has the same order
   and a duration consistent with the ordered Scene durations.
5. Write `<project-root>/rendered_media_validation_result.md` with `Result:
   PASS` or `Result: FAIL`; all commands, exit codes, complete output, metadata,
   hashes, duration checks, audio checks, source/gate checks, and Scene-order
   checks. Identify each failed check and its evidence.

## Completion criteria

`Result: PASS` is allowed only when preflight passes; every media command exits
`0`; all media hashes and metadata are recorded; source and gate identity is
consistent; each Scene's duration and audio agree with narration evidence; and
the four Scene files and combined file preserve approved order. Any missing,
unreadable, inconsistent, corrupt, unverified, or failed item is `Result: FAIL`.

## Final response

- `DONE`: give the absolute `rendered_media_validation_result.md` path, its
  `PASS` or `FAIL` result, and a concise per-file command/check summary.
- `BLOCKED`: use only when the environment prevents even writing
  `rendered_media_validation_result.md`; give the evidence, affected absolute
  paths, and the action required from the coordinator.
