# V2 Change Log

Use this file to record deliberate changes to the v2 skill and the reason behind each change.

## Template

```markdown
## YYYY-MM-DD

### Changed

- 

### Why

- 

### Expected Impact

- 

### Verification

- 

### Follow-up

- 
```

## 2026-04-20

### Changed

- Created a development copy of the current official skill at `skill-src/algorithm-teaching-animation-v2`.
- Changed the v2 skill frontmatter name to `algorithm-teaching-animation-v2`.
- Added this design note structure outside the runtime skill package.

### Why

- Keep v2 development separate from the official installed skill.
- Allow iterative design without breaking the currently available production skill.
- Keep design notes out of the installable skill package to reduce runtime noise.

### Expected Impact

- V2 can be edited, reviewed, and tested independently.
- The official skill remains unchanged until v2 is ready to install.

### Verification

- `quick_validate.py` passed for the v2 skill folder when run with UTF-8 mode enabled.

### Follow-up

- Decide which v2 improvements should be made first.
- Synchronize examples with the current workflow, especially subtitles and review notes.

## 2026-04-20

### Changed

- Changed v2 complete workflow from subtitle-first to voiceover-audio-first.
- Added `references/voiceover.md` for beat-aligned English narration, TTS provider contract, `narration_manifest.json`, and beat-level WAV outputs.
- Updated Manim and rendering references to treat narration manifest and audio sync as default complete-workflow requirements.
- Updated the development index and quality rubric to include voiceover/audio quality.

### Why

- The desired v2 behavior is a narrated teaching animation with human voice explanation, not an on-screen subtitle workflow.
- TTS should remain provider-agnostic, but final narrated delivery must not skip actual audio generation.

### Expected Impact

- Future v2 users should get `voiceover.md`, `narration_manifest.json`, and `audio/voiceover/*.wav` for complete workflows.
- Missing TTS provider setup becomes an explicit blocker for final narrated delivery instead of an implicit downgrade.

### Verification

- `quick_validate.py` passed for the v2 skill folder with UTF-8 mode enabled.

### Follow-up

- Add a canonical narrated binary-search example.
- Decide whether to keep existing examples as partial examples or update them to the new complete workflow.
