# 🎬 arabic-whisper-srt

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Arabic NLP](https://img.shields.io/badge/NLP-Arabic%20Punctuation-green.svg)](https://github.com/MobileConduit)
[![Whisper Engine](https://img.shields.io/badge/Engine-faster--whisper-red.svg)](https://github.com/SYSTRAN/faster-whisper)

A dedicated Arabic Speech-to-Text subtitle engine powered by `faster-whisper`. Designed specifically to handle Arabic dialects, formal Arabic (Fusha), correct punctuation placement (فاصلة عربية، علامات استفهام), and generate timed `.srt` and `.vtt` tracks.

---

## 🌟 Highlights
- **Sub-word Timing & Proper RTL Segmentation**: Avoids broken Arabic lines across subtitle frames.
- **Optimized with `faster-whisper`**: Up to 4x faster execution and lower VRAM usage compared to vanilla Whisper.
- **Arabic Text Normalization**: Cleans repeated characters, fixes punctuation gaps, and enhances readability.

## 🚀 Installation & Usage

```bash
git clone https://github.com/MobileConduit/arabic-whisper-srt.git
cd arabic-whisper-srt
pip install -r requirements.txt
```

### Transcribe Media:
```bash
python whisper_srt.py --input interview.mp4 --model medium --output interview.srt
```

---

## 👤 Author & Maintainer

**Eng. MHD. Shadi AL-Hasan**  
- **Role:** Executive CTO & Enterprise Solutions Architect  
- **Email:** [mhd.shadi.alhasan@gmail.com](mailto:mhd.shadi.alhasan@gmail.com)  
- **Phone / WhatsApp:** [+963934005922](tel:+963934005922)  
- **Location:** Damascus, Syria  
- **GitHub:** [MobileConduit](https://github.com/MobileConduit)  

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.  
Copyright (c) 2026 **MHD. Shadi AL-Hasan**. All rights reserved.

