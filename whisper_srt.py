# -*- coding: utf-8 -*-
"""
Arabic Whisper Subtitler & SRT Generator
Author: Eng. MHD. Shadi AL-Hasan <mhd.shadi.alhasan@gmail.com>
Phone: +963934005922
Copyright (c) 2026 MHD. Shadi AL-Hasan
"""

import os
import sys
import re
import argparse
from pathlib import Path

def format_timestamp(seconds: float) -> str:
    """Converts seconds into SRT timestamp format: HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def clean_arabic_text(text: str) -> str:
    """Cleans and standardizes transcribed Arabic text."""
    if not text:
        return ""
    # Strip unnecessary whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    # Normalize punctuation spacing
    text = re.sub(r'\s+([،؛؟.,!])', r'\1', text)
    return text

def generate_srt(segments: list, output_file: Path):
    """Writes subtitle segments to an SRT file."""
    with open(output_file, "w", encoding="utf-8") as f:
        for idx, seg in enumerate(segments, 1):
            start = format_timestamp(seg["start"])
            end = format_timestamp(seg["end"])
            text = clean_arabic_text(seg["text"])
            
            f.write(f"{idx}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")

def transcribe(audio_path: str, model_size="medium", language="ar", output_srt=None):
    print(f"[*] Initializing Whisper model: [{model_size}] for language [{language}]...")
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel(model_size, device="auto", compute_type="auto")
        print(f"[*] Processing audio file: {audio_path}")
        segments_raw, info = model.transcribe(audio_path, language=language, beam_size=5)
        
        segments = []
        for s in segments_raw:
            segments.append({
                "start": s.start,
                "end": s.end,
                "text": s.text
            })
            print(f"[{format_timestamp(s.start)} -> {format_timestamp(s.end)}] {s.text}")

        out_path = Path(output_srt) if output_srt else Path(audio_path).with_suffix(".srt")
        generate_srt(segments, out_path)
        print(f"[+] Successfully generated Arabic subtitles: {out_path}")

    except ImportError:
        print("[!] faster-whisper not installed. Falling back to CLI demo simulation mode.")
        demo_segments = [
            {"start": 0.5, "end": 3.8, "text": "أهلاً بكم في هذا العرض التقديمي حول الذكاء الاصطناعي."},
            {"start": 4.1, "end": 7.5, "text": "تم تطوير هذا النظام بواسطة المهندس شادي الحسن."},
            {"start": 8.0, "end": 12.2, "text": "نظام تفريغ دقيق متكامل مع قواعد معالجة اللغة العربية."}
        ]
        out_path = Path(output_srt) if output_srt else Path("demo_arabic_output.srt")
        generate_srt(demo_segments, out_path)
        print(f"[DEMO] Sample SRT file created: {out_path}")

def main():
    parser = argparse.ArgumentParser(description="Transcribe Arabic media to formatted SRT subtitles.")
    parser.add_argument("--input", "-i", type=str, required=True, help="Path to input audio/video file")
    parser.add_argument("--model", "-m", type=str, default="medium", choices=["tiny", "base", "small", "medium", "large-v3"])
    parser.add_argument("--output", "-o", type=str, default=None, help="Output .srt path")
    args = parser.parse_args()

    transcribe(args.input, model_size=args.model, output_srt=args.output)

if __name__ == "__main__":
    main()
