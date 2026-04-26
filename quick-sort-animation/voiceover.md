# Voiceover

## Summary

- Language: en
- Voice style: clear teaching voice
- Source: condensed from `teaching_script.md`
- TTS provider: Windows SAPI.SpVoice, Microsoft Zira Desktop when available

## Beats

### beat-001: Establish the input

- Trace mapping: `beat_id: beat-001`
- Narration:
  We start with seven values. Quick Sort will repeatedly choose the rightmost value as a pivot, place it where it belongs, and then sort the two sides.
- Pacing: 7-9 seconds
- Pronunciation notes: say "Quick Sort" as two words

### beat-002: Start the first partition

- Trace mapping: `beat_id: beat-002`
- Narration:
  The first active range is the whole array, and the pivot is forty. The boundary i starts before the range, so the less than or equal side is empty.
- Pacing: 8-10 seconds
- Pronunciation notes: say "i" as the letter name

### beat-003: Scan values greater than the pivot

- Trace mapping: `beat_id: beat-003`
- Narration:
  The scan pointer checks fifty, ninety, and seventy. Each one is greater than forty, so the boundary does not move.
- Pacing: 7-9 seconds
- Pronunciation notes: none

### beat-004: Move 20 to the left side

- Trace mapping: `beat_id: beat-004`
- Narration:
  Now twenty is less than or equal to the pivot. The boundary advances, and twenty is swapped into the left side of the partition.
- Pacing: 7-9 seconds
- Pronunciation notes: none

### beat-005: Move 10 and 30 to the left side

- Trace mapping: `beat_id: beat-005`
- Narration:
  Ten and thirty also belong before forty. Each time that happens, the boundary grows and the value is moved into the left region.
- Pacing: 8-10 seconds
- Pronunciation notes: none

### beat-006: Place pivot 40

- Trace mapping: `beat_id: beat-006`
- Narration:
  After the scan, the pivot swaps with the first value greater than it. Forty is now fixed: smaller values are on the left, larger values are on the right.
- Pacing: 8-10 seconds
- Pronunciation notes: none

### beat-007: Partition the left range

- Trace mapping: `beat_id: beat-007`
- Narration:
  Quick Sort now works on the left side. With thirty as the pivot, both twenty and ten already belong on the less than or equal side.
- Pacing: 8-10 seconds
- Pronunciation notes: none

### beat-008: Focus on range [20, 10]

- Trace mapping: `beat_id: beat-008`
- Narration:
  The remaining left range uses ten as the pivot. Since twenty is greater than ten, the pivot needs to move in front of it.
- Pacing: 7-9 seconds
- Pronunciation notes: none

### beat-009: Complete the left side

- Trace mapping: `beat_id: beat-009`
- Narration:
  Ten swaps into the first position, and the single value twenty becomes a base case. The left side is now fully sorted.
- Pacing: 7-9 seconds
- Pronunciation notes: none

### beat-010: Partition the right range

- Trace mapping: `beat_id: beat-010`
- Narration:
  On the right side, fifty is the pivot. Ninety and seventy are both greater than fifty, so nothing joins the left region.
- Pacing: 7-9 seconds
- Pronunciation notes: none

### beat-011: Place pivot 50

- Trace mapping: `beat_id: beat-011`
- Narration:
  The pivot fifty moves to the front of this range. That leaves only seventy and ninety to finish on the right.
- Pacing: 6-8 seconds
- Pronunciation notes: none

### beat-012: Finish [70, 90]

- Trace mapping: `beat_id: beat-012`
- Narration:
  With ninety as the pivot, seventy is already on the correct side. Ninety is fixed at the end, and seventy is a one element base case.
- Pacing: 8-10 seconds
- Pronunciation notes: none

### beat-013: Final sorted array

- Trace mapping: `beat_id: beat-013`
- Narration:
  Every pivot has been fixed, and every recursive range is finished. The final ascending order is ten, twenty, thirty, forty, fifty, seventy, ninety.
- Pacing: 8-10 seconds
- Pronunciation notes: none

