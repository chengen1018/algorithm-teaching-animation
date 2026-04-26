$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$AudioDir = Join-Path $Root "audio\voiceover"
New-Item -ItemType Directory -Force -Path $AudioDir | Out-Null

$Segments = @(
    [ordered]@{
        beat_id = "beat-001"
        trace_mapping = "beat_id: beat-001"
        text = "We start with seven values. Quick Sort will repeatedly choose the rightmost value as a pivot, place it where it belongs, and then sort the two sides."
        audio_path = "audio/voiceover/beat-001.wav"
    },
    [ordered]@{
        beat_id = "beat-002"
        trace_mapping = "beat_id: beat-002"
        text = "The first active range is the whole array, and the pivot is forty. The boundary i starts before the range, so the less than or equal side is empty."
        audio_path = "audio/voiceover/beat-002.wav"
    },
    [ordered]@{
        beat_id = "beat-003"
        trace_mapping = "beat_id: beat-003"
        text = "The scan pointer checks fifty, ninety, and seventy. Each one is greater than forty, so the boundary does not move."
        audio_path = "audio/voiceover/beat-003.wav"
    },
    [ordered]@{
        beat_id = "beat-004"
        trace_mapping = "beat_id: beat-004"
        text = "Now twenty is less than or equal to the pivot. The boundary advances, and twenty is swapped into the left side of the partition."
        audio_path = "audio/voiceover/beat-004.wav"
    },
    [ordered]@{
        beat_id = "beat-005"
        trace_mapping = "beat_id: beat-005"
        text = "Ten and thirty also belong before forty. Each time that happens, the boundary grows and the value is moved into the left region."
        audio_path = "audio/voiceover/beat-005.wav"
    },
    [ordered]@{
        beat_id = "beat-006"
        trace_mapping = "beat_id: beat-006"
        text = "After the scan, the pivot swaps with the first value greater than it. Forty is now fixed: smaller values are on the left, larger values are on the right."
        audio_path = "audio/voiceover/beat-006.wav"
    },
    [ordered]@{
        beat_id = "beat-007"
        trace_mapping = "beat_id: beat-007"
        text = "Quick Sort now works on the left side. With thirty as the pivot, both twenty and ten already belong on the less than or equal side."
        audio_path = "audio/voiceover/beat-007.wav"
    },
    [ordered]@{
        beat_id = "beat-008"
        trace_mapping = "beat_id: beat-008"
        text = "The remaining left range uses ten as the pivot. Since twenty is greater than ten, the pivot needs to move in front of it."
        audio_path = "audio/voiceover/beat-008.wav"
    },
    [ordered]@{
        beat_id = "beat-009"
        trace_mapping = "beat_id: beat-009"
        text = "Ten swaps into the first position, and the single value twenty becomes a base case. The left side is now fully sorted."
        audio_path = "audio/voiceover/beat-009.wav"
    },
    [ordered]@{
        beat_id = "beat-010"
        trace_mapping = "beat_id: beat-010"
        text = "On the right side, fifty is the pivot. Ninety and seventy are both greater than fifty, so nothing joins the left region."
        audio_path = "audio/voiceover/beat-010.wav"
    },
    [ordered]@{
        beat_id = "beat-011"
        trace_mapping = "beat_id: beat-011"
        text = "The pivot fifty moves to the front of this range. That leaves only seventy and ninety to finish on the right."
        audio_path = "audio/voiceover/beat-011.wav"
    },
    [ordered]@{
        beat_id = "beat-012"
        trace_mapping = "beat_id: beat-012"
        text = "With ninety as the pivot, seventy is already on the correct side. Ninety is fixed at the end, and seventy is a one element base case."
        audio_path = "audio/voiceover/beat-012.wav"
    },
    [ordered]@{
        beat_id = "beat-013"
        trace_mapping = "beat_id: beat-013"
        text = "Every pivot has been fixed, and every recursive range is finished. The final ascending order is ten, twenty, thirty, forty, fifty, seventy, ninety."
        audio_path = "audio/voiceover/beat-013.wav"
    }
)

function Get-WavDurationSeconds {
    param([string]$Path)

    $bytes = [System.IO.File]::ReadAllBytes($Path)
    $position = 12
    $byteRate = 0

    while ($position + 8 -lt $bytes.Length) {
        $chunkId = [System.Text.Encoding]::ASCII.GetString($bytes, $position, 4)
        $chunkSize = [System.BitConverter]::ToInt32($bytes, $position + 4)

        if ($chunkId -eq "fmt ") {
            $byteRate = [System.BitConverter]::ToInt32($bytes, $position + 16)
        }
        elseif ($chunkId -eq "data") {
            if ($byteRate -eq 0) {
                throw "Could not read byte rate before data chunk in $Path"
            }
            return [Math]::Round($chunkSize / $byteRate, 2)
        }

        $position += 8 + $chunkSize + ($chunkSize % 2)
    }

    throw "Could not find data chunk in $Path"
}

$Voice = New-Object -ComObject SAPI.SpVoice
$AvailableVoices = $Voice.GetVoices()
for ($i = 0; $i -lt $AvailableVoices.Count; $i++) {
    $Candidate = $AvailableVoices.Item($i)
    if ($Candidate.GetDescription() -like "*Zira*English*") {
        $Voice.Voice = $Candidate
        break
    }
}

foreach ($Segment in $Segments) {
    $FullAudioPath = Join-Path $Root $Segment.audio_path
    $Stream = New-Object -ComObject SAPI.SpFileStream
    $Stream.Open($FullAudioPath, 3, $false)
    $Voice.AudioOutputStream = $Stream
    [void]$Voice.Speak($Segment.text)
    $Stream.Close()
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($Stream)
    $Segment.duration_seconds = Get-WavDurationSeconds -Path $FullAudioPath
}

$Manifest = [ordered]@{
    language = "en"
    audio_mode = "voiceover"
    tts_provider = "Windows SAPI.SpVoice"
    voice = "Microsoft Zira Desktop - English (United States)"
    segments = $Segments
}

$ManifestPath = Join-Path $Root "narration_manifest.json"
$Manifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $ManifestPath -Encoding UTF8

[void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($Voice)

