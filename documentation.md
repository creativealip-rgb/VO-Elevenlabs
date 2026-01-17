# 🎙️ ElevenLabs TTS Generator

Text-to-Speech generator menggunakan ElevenLabs API dengan fitur **auto-rotate API keys**.

---

## 📋 Requirements

### System Requirements
- **Python** 3.10+
- **Internet connection**

### Python Dependencies
```
requests>=2.31.0
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ⚙️ Setup

### 1. Tambahkan API Keys

Edit file `api_keys.txt`, satu API key per baris:

```
sk_your_first_api_key_here
sk_your_second_api_key_here
sk_your_third_api_key_here
```

> 💡 Dapatkan API key dari [elevenlabs.io](https://elevenlabs.io) → Profile → API Keys

### 2. (Opsional) Ubah Default Voice

Edit `tts.py` line 78 untuk mengubah voice default:

```python
default="YOUR_VOICE_ID",
```

---

## 🚀 Cara Pakai

### CLI Commands

| Command | Deskripsi |
|---------|-----------|
| `python tts.py "Teks"` | Generate dengan output default |
| `python tts.py "Teks" -o output/nama.mp3` | Custom output filename |
| `python tts.py -f script.txt` | Generate dari file TXT |
| `python tts.py -f script.txt -o output/narasi.mp3` | File + custom output |
| `python tts.py --check` | Cek kredit semua API keys |
| `python tts.py -v VOICE_ID "Teks"` | Gunakan voice berbeda |
| `python tts.py --help` | Tampilkan bantuan |

### Contoh Penggunaan

```bash
# Generate intro video
python tts.py "Halo sobat, selamat datang di channel saya" -o output/intro.mp3

# Generate dari script panjang
python tts.py -f narasi.txt -o output/narasi_video.mp3

# Cek sisa kredit semua akun
python tts.py --check

# Gunakan voice berbeda
python tts.py -v pNInz6obpgDQGcFmaJgB "Hello world" -o output/test.mp3
```

---

## 📁 Struktur Folder

```
elevenlabs-infinity/
├── output/              # Hasil generate tersimpan di sini
├── voice_gen/
│   ├── api_utils/       # ElevenLabs API wrapper
│   │   └── eleven_api.py
│   └── audio/           # Voice module
│       └── eleven_voice_module.py
├── api_keys.txt         # Daftar API keys (1 per baris)
├── current_key_index.txt # Tracking key aktif (auto-generated)
├── main.py              # Core functions
├── tts.py               # CLI tool
├── requirements.txt     # Dependencies
└── documentation.md     # Dokumentasi ini
```

---

## 🔄 Fitur Auto-Rotate

Program akan **otomatis pindah** ke API key berikutnya ketika:
- Kredit kurang dari 100 karakter
- API key error atau limit tercapai

### Cara Kerja

```
Key #1 (9000 credits) → digunakan
Key #1 habis → otomatis pindah ke Key #2
Key #2 (10000 credits) → digunakan
... dan seterusnya
```

---

## 🎤 Daftar Voice ID

### Default Voices (Free Tier)

| Voice | ID |
|-------|-----|
| Adam | `pNInz6obpgDQGcFmaJgB` |
| Rachel | `21m00Tcm4TlvDq8ikWAM` |
| Domi | `AZnzlk1XvdvUeBnXmlld` |

### Custom Voice

Untuk voice custom/clone, gunakan Voice ID dari ElevenLabs dashboard.

---

## ⚠️ Troubleshooting

| Error | Solusi |
|-------|--------|
| `FileNotFoundError: api_keys.txt` | Buat file `api_keys.txt` dengan API keys |
| `All API keys exhausted` | Tambahkan lebih banyak API keys |
| `Voice ID not found` | Gunakan Voice ID yang valid |
| `401 Unauthorized` | API key tidak valid |

---

## 📊 Cek Kredit

```bash
python tts.py --check
```

Output:
```
==================================================
📊 Checking credits for all 11 API keys...
==================================================

✅ Key #1: 9,834 characters
✅ Key #2: 10,000 characters
...

==================================================
💰 Total available credits: 109,834 characters
==================================================
```

---

## 🔧 API Reference

### `generate_voice(text, output_file, voice_id, min_credits)`

| Parameter | Type | Default | Deskripsi |
|-----------|------|---------|-----------|
| `text` | str | required | Teks yang akan di-convert |
| `output_file` | str | `"output/output.mp3"` | Path file output |
| `voice_id` | str | `"c470sxKWDq6tA74TL3yB"` | ElevenLabs Voice ID |
| `min_credits` | int | `100` | Minimum kredit sebelum rotate |

### `check_all_credits()`

Menampilkan sisa kredit untuk semua API keys.

---

## 📝 License

MIT License - Free to use and modify.
