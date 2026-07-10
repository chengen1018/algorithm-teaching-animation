# Local Cross-Platform TTS Design

## Purpose

Make the `VOICEOVER` stage generate real, usable narration without an API key or per-use cloud charge. The solution must work on Windows and macOS, support English and Mandarin Chinese, and prevent a silent placeholder from being accepted as voiceover.

## Decisions

- Use the local Kokoro model as the primary TTS provider.
- Use one shared TTS environment at `/Users/lichengen/Developer/Senior-project/animation/.tts-env/`, outside any single animation project.
- Keep every animation's narration assets inside that animation's own folder.
- Download model files and dependencies once during setup; narration generation then runs locally without a provider API key.
- Keep the existing Manim environment separate. TTS produces audio only; Manim rendering and FFmpeg remain responsible for visual rendering and final muxing.
- Support English with Kokoro's American-English voice configuration and Mandarin Chinese with its Chinese language configuration. A narration beat uses one configured language and voice; mixed-language narration is not a first-scope requirement.

## Directory Layout

```text
/Users/lichengen/Developer/Senior-project/animation/
├── .tts-env/                  # Shared, local Python environment and TTS dependencies
├── tts-samples/               # Disposable English and Chinese audition WAVs
├── binary-search/
│   ├── narration_manifest.json
│   ├── audio/voiceover/       # Audio assets for this animation only
│   └── renders/
└── <other-animation>/
    ├── narration_manifest.json
    ├── audio/voiceover/
    └── renders/
```

`.tts-env/`, model caches, audition WAVs, and rendered media must not be committed to Git. Version-pinned setup instructions and the generator code are committed so Windows and macOS can reproduce the provider.

## Components and Data Flow

1. A per-animation `narration_manifest.json` supplies ordered beat IDs, narration text, language, voice, target timing, and output relative paths.
2. The TTS generator validates the manifest before synthesis: unique ordered beat IDs, non-empty narration, supported language, safe output path, and a fixed provider/voice configuration.
3. Kokoro generates a PCM WAV for each beat in the animation's `audio/voiceover/` directory.
4. The validator uses audio metadata and decoded samples to reject files that are missing, empty, undecodable, or effectively silent. It records duration, sample rate, channel count, peak level, and RMS level for every beat.
5. The stage succeeds only when every manifest beat has a validated, non-silent audio file. It writes an updated manifest/report with the actual duration; otherwise it exits non-zero and leaves `VOICEOVER` incomplete.
6. The render/mux step consumes those validated files, preserves scheduled gaps, produces a full narration track, and muxes it into the final MP4 as AAC. It must verify the final video is still 1920x1080 at 60 fps and contains a non-empty audio stream.

## Failure Handling

- Missing model, dependency, language pack, or voice: fail with an installation/configuration error; never create silent timing files.
- Synthesis error, empty output, decoding error, silence, or duration outside an allowed tolerance: fail the affected beat and the `VOICEOVER` stage.
- Narration longer than the visual beat: report the exact beat and actual duration. The remedy is to revise wording/pacing in `VOICEOVER`, or return to `SCRIPT` when the beat contains too many teaching actions.
- No fallback to OS-provided voices: macOS `say` and Windows SAPI would produce inconsistent voices and quality between platforms.
- No automatic cloud fallback: this design must remain keyless and cost-free. A future cloud provider can be an explicitly configured alternative, but it cannot be silently selected.

## Pilot Acceptance Test

Before integration with the workflow, create the shared TTS environment and generate one short English WAV and one short Mandarin-Chinese WAV in `tts-samples/`. Confirm each file decodes, is non-silent, and reports duration. The user listens to both samples and accepts or rejects the voice quality. No existing animation or Manim environment is modified by this pilot.

## Verification

- On both macOS and Windows, use the same locked dependency/model versions and generator command.
- Validate every generated beat before it reaches RENDER.
- Use FFprobe for final-stream verification: video is `1920x1080`, `60/1` fps; audio exists and uses AAC; final duration is plausible.
- Keep validation output with each animation so QA can trace every muxed segment back to a verified narration asset.

## Out of Scope

- Voice cloning, custom voice training, and automatic voice selection.
- Mixed English/Chinese within a single beat.
- Replacing the current animation workflow or changing approved visual content during the pilot.
