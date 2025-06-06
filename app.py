import subprocess
import gradio as gr
import wave
import math
import struct
from typing import List

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def freq_to_note(freq: float) -> str:
    if freq <= 0:
        return ""
    n = round(12 * math.log2(freq / 440.0) + 69)
    octave = n // 12 - 1
    name = NOTE_NAMES[n % 12]
    return f"{name}{octave}"


def zero_crossings(samples: List[int]) -> int:
    count = 0
    for i in range(1, len(samples)):
        if (samples[i - 1] >= 0 > samples[i]) or (samples[i - 1] < 0 <= samples[i]):
            count += 1
    return count


def extract_notes(wav_path: str) -> List[str]:
    notes: List[str] = []
    with wave.open(wav_path, "rb") as w:
        fr = w.getframerate()
        sampwidth = w.getsampwidth()
        frames = w.getnframes()
        window = fr // 10  # 0.1 second
        for _ in range(0, frames, window):
            raw = w.readframes(window)
            if len(raw) < sampwidth * 2:
                break
            samples = struct.unpack("<" + "h" * (len(raw) // sampwidth), raw)
            zc = zero_crossings(samples)
            freq = zc * fr / (2 * len(samples))
            note = freq_to_note(freq)
            if note:
                notes.append(note)
    return notes


def note_to_freq(note: str) -> float:
    if not note:
        return 0.0
    name = note[:-1]
    octave = int(note[-1])
    n = NOTE_NAMES.index(name) + (octave + 1) * 12
    return 440.0 * 2 ** ((n - 69) / 12)


def notes_to_wav(notes: List[str], output_path: str, dur: float = 0.3) -> None:
    fr = 44100
    with wave.open(output_path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(fr)
        for note in notes:
            freq = note_to_freq(note)
            for i in range(int(dur * fr)):
                val = int(32767 * math.sin(2 * math.pi * freq * (i / fr)))
                w.writeframes(struct.pack("<h", val))


def convert(url: str):
    if not url:
        return None, ""
    try:
        result = subprocess.run([
            './lofi-converter', url
        ], capture_output=True, text=True, check=True)
        wav_path = result.stdout.strip().splitlines()[-1]
        notes = extract_notes(wav_path)
        notes_audio = wav_path.replace('.wav', '_notes.wav')
        notes_to_wav(notes, notes_audio)
        return notes_audio, " ".join(notes)
    except subprocess.CalledProcessError as e:
        return None, f"Error: {e.stderr}"


def main():
    with gr.Blocks(title="YouTube Note Extractor") as demo:
        gr.Markdown("# YouTube Note Extractor")
        url_in = gr.Textbox(label="YouTube URL")
        convert_btn = gr.Button("Convert to Notes")
        audio_out = gr.Audio(label="Synthesized Notes")
        notes_out = gr.Textbox(label="Detected Notes")

        convert_btn.click(fn=convert, inputs=url_in, outputs=[audio_out, notes_out])
    demo.launch()


if __name__ == "__main__":
    main()
