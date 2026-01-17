"""
ElevenLabs Voice Generator CLI
Usage:
    python tts.py "Teks yang ingin diubah menjadi suara"
    python tts.py "Teks" -o output.mp3
    python tts.py -f script.txt -o narasi.mp3
    python tts.py --check  (cek kredit semua akun)
"""

import argparse
import sys
import os
from main import generate_voice, check_all_credits


def read_text_from_file(filepath):
    """Baca teks dari file TXT"""
    if not os.path.exists(filepath):
        print(f"❌ Error: File '{filepath}' tidak ditemukan!")
        sys.exit(1)
    
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read().strip()
    
    if not text:
        print(f"❌ Error: File '{filepath}' kosong!")
        sys.exit(1)
    
    return text


def ensure_output_dir(filepath):
    """Pastikan folder output ada, buat jika belum"""
    dirname = os.path.dirname(filepath)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)
        print(f"📁 Folder '{dirname}' dibuat")


def main():
    parser = argparse.ArgumentParser(
        description="🎙️ ElevenLabs Text-to-Speech Generator dengan Auto-Rotate API Keys",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh Manual:
  python tts.py "Halo sobat selular!"
  python tts.py "Selamat datang" -o welcome.mp3

Contoh dari File:
  python tts.py -f script.txt
  python tts.py -f narasi.txt -o video_narasi.mp3

Opsi Lain:
  python tts.py "Test" -v VOICE_ID_KAMU
  python tts.py --check
        """
    )
    
    parser.add_argument(
        "text", 
        nargs="?",
        help="Teks yang akan diubah menjadi suara (cara manual)"
    )
    
    parser.add_argument(
        "-f", "--file",
        help="Path ke file TXT yang berisi teks (cara dari file)"
    )
    
    parser.add_argument(
        "-o", "--output",
        default="output/output.mp3",
        help="Nama file output (default: output/output.mp3)"
    )
    
    parser.add_argument(
        "-v", "--voice",
        default="c470sxKWDq6tA74TL3yB",
        help="Voice ID (default: Kennisa)"
    )
    
    parser.add_argument(
        "-m", "--min-credits",
        type=int,
        default=100,
        help="Minimum kredit sebelum rotate (default: 100)"
    )
    
    parser.add_argument(
        "--check",
        action="store_true",
        help="Cek kredit semua API keys"
    )
    
    args = parser.parse_args()
    
    # Cek kredit
    if args.check:
        check_all_credits()
        return
    
    # Tentukan sumber teks (file atau manual)
    if args.file:
        print(f"📄 Membaca teks dari file: {args.file}")
        text = read_text_from_file(args.file)
    elif args.text:
        text = args.text
    else:
        parser.print_help()
        print("\n❌ Error: Teks harus diisi!")
        print("   Cara 1 (Manual): python tts.py \"Halo dunia!\"")
        print("   Cara 2 (File):   python tts.py -f script.txt")
        sys.exit(1)
    
    # Generate voice
    # Pastikan folder output ada
    ensure_output_dir(args.output)
    
    # Tampilkan preview teks (potong jika terlalu panjang)
    preview = text[:100] + "..." if len(text) > 100 else text
    print(f"\n📝 Teks: {preview}")
    print(f"📊 Panjang: {len(text)} karakter")
    print(f"📁 Output: {args.output}")
    print(f"🎤 Voice: {args.voice}\n")
    
    success = generate_voice(
        text=text,
        output_file=args.output,
        voice_id=args.voice,
        min_credits=args.min_credits
    )
    
    if success:
        print(f"\n🎉 Selesai! File tersimpan di: {args.output}")
    else:
        print(f"\n❌ Gagal generate suara")
        sys.exit(1)


if __name__ == "__main__":
    main()
