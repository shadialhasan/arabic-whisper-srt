# -*- coding: utf-8 -*-
"""
Automated Test Suite for arabic-whisper-srt
Author: Eng. MHD. Shadi AL-Hasan <mhd.shadi.alhasan@gmail.com>
"""

import io
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from whisper_srt import (
    format_timestamp,
    clean_arabic_text,
    validate_segment,
    generate_srt,
    generate_vtt,
    get_demo_segments,
    transcribe,
    main
)


class TestTimestampFormatting(unittest.TestCase):

    def test_format_timestamp_srt(self):
        self.assertEqual(format_timestamp(0.0), "00:00:00,000")
        self.assertEqual(format_timestamp(65.5), "00:01:05,500")
        self.assertEqual(format_timestamp(3661.123), "01:01:01,123")
        # Negative timestamp clamped to zero
        self.assertEqual(format_timestamp(-5.0), "00:00:00,000")

    def test_format_timestamp_vtt(self):
        self.assertEqual(format_timestamp(0.0, separator="."), "00:00:00.000")
        self.assertEqual(format_timestamp(65.5, separator="."), "00:01:05.500")
        self.assertEqual(format_timestamp(3661.123, separator="."), "01:01:01.123")


class TestArabicTextCleaning(unittest.TestCase):

    def test_clean_punctuation_spacing(self):
        raw = "مرحبا بكم    في المؤتمر   ،   نحن سعداء بلقائكم  ؟   "
        cleaned = clean_arabic_text(raw)
        self.assertEqual(cleaned, "مرحبا بكم في المؤتمر، نحن سعداء بلقائكم؟")

    def test_clean_tatweel(self):
        raw = "تـطـويـر الأنـظـمـة"
        cleaned = clean_arabic_text(raw)
        self.assertEqual(cleaned, "تطوير الأنظمة")

    def test_collapse_repeated_punctuation(self):
        raw = "هل تسمعني؟؟؟؟ نعم،، بالتاكيد!!!"
        cleaned = clean_arabic_text(raw)
        self.assertEqual(cleaned, "هل تسمعني؟ نعم، بالتاكيد!")

    def test_empty_and_invalid_inputs(self):
        self.assertEqual(clean_arabic_text(""), "")
        self.assertEqual(clean_arabic_text(None), "")  # type: ignore
        self.assertEqual(clean_arabic_text("   "), "")


class TestSegmentValidation(unittest.TestCase):

    def test_valid_segment(self):
        seg = {"start": 1.0, "end": 4.5, "text": "نص عربي سليم"}
        # Should not raise
        validate_segment(seg, 1)

    def test_invalid_segment_types(self):
        with self.assertRaises(ValueError):
            validate_segment("not a dict", 1)  # type: ignore
        with self.assertRaises(ValueError):
            validate_segment({"start": 1.0}, 1)
        with self.assertRaises(ValueError):
            validate_segment({"start": "one", "end": 2.0}, 1)  # type: ignore

    def test_invalid_timestamp_order_and_bounds(self):
        with self.assertRaises(ValueError):
            validate_segment({"start": -1.0, "end": 2.0}, 1)
        with self.assertRaises(ValueError):
            validate_segment({"start": 5.0, "end": 2.0}, 1)


class TestSubtitleGenerators(unittest.TestCase):

    def setUp(self):
        self.segments = [
            {"start": 1.0, "end": 3.5, "text": "الجملة الأولى الترحيبية."},
            {"start": 4.0, "end": 6.8, "text": "الجملة الثانية التوضيحية."}
        ]

    def test_generate_srt(self):
        with TemporaryDirectory() as tmpdir:
            srt_path = Path(tmpdir) / "test.srt"
            generate_srt(self.segments, srt_path)
            self.assertTrue(srt_path.exists())

            content = srt_path.read_text(encoding="utf-8")
            self.assertIn("1\n00:00:01,000 --> 00:00:03,500\nالجملة الأولى الترحيبية.", content)
            self.assertIn("2\n00:00:04,000 --> 00:00:06,800\nالجملة الثانية التوضيحية.", content)

    def test_generate_vtt(self):
        with TemporaryDirectory() as tmpdir:
            vtt_path = Path(tmpdir) / "test.vtt"
            generate_vtt(self.segments, vtt_path)
            self.assertTrue(vtt_path.exists())

            content = vtt_path.read_text(encoding="utf-8")
            self.assertTrue(content.startswith("WEBVTT"))
            self.assertIn("00:00:01.000 --> 00:00:03.500", content)


class TestWhisperCliAndTranscription(unittest.TestCase):

    def test_transcribe_demo_both_formats(self):
        with TemporaryDirectory() as tmpdir:
            base_out = Path(tmpdir) / "demo_test"
            files = transcribe(
                audio_path="demo",
                output_srt=str(base_out),
                output_format="both",
                demo_mode=True
            )
            self.assertEqual(len(files), 2)
            self.assertTrue((Path(tmpdir) / "demo_test.srt").exists())
            self.assertTrue((Path(tmpdir) / "demo_test.vtt").exists())

    def test_cli_demo_execution(self):
        with TemporaryDirectory() as tmpdir:
            out_srt = Path(tmpdir) / "cli_demo.srt"
            code = main(["--input", "demo", "--output", str(out_srt), "--demo"])
            self.assertEqual(code, 0)
            self.assertTrue(out_srt.exists())

    def test_cli_missing_file_error(self):
        stderr_buf = io.StringIO()
        old_stderr = sys.stderr
        try:
            sys.stderr = stderr_buf
            code = main(["--input", "non_existent_audio_file_98765.mp3"])
            self.assertEqual(code, 1)
        finally:
            sys.stderr = old_stderr


if __name__ == "__main__":
    unittest.main()
