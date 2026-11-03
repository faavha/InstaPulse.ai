#!/usr/bin/env python3
"""
beats.py - ubah naskah Reel jadi beat sheet berwaktu sebelum direkam.

Menghitung berapa lama tiap baris diucapkan, menumpuknya jadi timecode, lalu
menandai empat hal yang membunuh Reel di meja edit: hook yang lewat dari
batas detik awal, satu beat yang cukup lama untuk bikin penonton pergi,
deretan baris tanpa satu pun hal konkret, dan durasi total yang tidak sesuai
target.

Versi bahasa Indonesia: durasi dihitung dari SUKU KATA, bukan kata, dan angka
dihitung seperti diucapkan ("Rp4.500.000" = "empat juta lima ratus ribu
rupiah" = 13 suku kata). Lihat idlang.py.

Default 5,5 suku kata per detik untuk bicara santai ke kamera. Kalibrasi
sekali dengan laju bicaramu sendiri: rekam dirimu membaca naskah dengan
tempo biasa, catat durasinya, lalu jalankan

  python3 beats.py naskah.txt --kalibrasi 27.5

Angka suku-kata-per-detik yang keluar simpan di voice.md dan pakai dengan --sps.

Pemakaian
  python3 beats.py naskah.txt
  python3 beats.py naskah.txt --target 30
  python3 beats.py naskah.txt --sps 6.2 --target 45
  python3 beats.py naskah.txt --json
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from idlang import (MONEY_WORDS, SPOKEN_NUMBERS, STOPWORDS,  # noqa: E402
                    normalize_numbers, syllables_word, words)

DEFAULT_SPS = 5.5
SENT_RE = re.compile(r"[^.!?]+[.!?]*")
CONCRETE_RE = re.compile(r"(?i:rp\.?\s?|\$\s?)\d|\b\d[\d,.]*|(?<!^)\b[A-Z][a-z]{2,}\b|\b[A-Z]{2,6}\b",
                         re.MULTILINE)

HOOK_WINDOW = 3.5        # detik. Lewat dari ini, jempol sudah memutuskan.
MAX_BEAT = 4.0           # detik pada satu ide tanpa perubahan di layar.
ABSTRACT_RUN = 3         # beat berturut-turut tanpa hal yang bisa dicek.


def concrete_count(text):
    n = len(CONCRETE_RE.findall(text))
    n += sum(1 for w in words(text) if w.lower() in SPOKEN_NUMBERS or w.lower() in MONEY_WORDS)
    return n


def syl(text):
    return sum(syllables_word(w) for w in words(text))


def tc(seconds):
    m, s = divmod(seconds, 60)
    return f"{int(m)}:{s:04.1f}"


def pretty(token):
    """Kembalikan titik ribuan untuk tampilan (gaya Indonesia)."""
    return re.sub(r"(\d)(?=(\d{3})+$)", r"\1.", token)


def split_beats(raw, sps):
    """Satu baris satu beat, kecuali barisnya terlalu panjang untuk satu beat."""
    beats = []
    for line in [ln.strip() for ln in raw.splitlines()]:
        if not line:
            continue
        if syl(line) / sps <= MAX_BEAT * 1.5:
            beats.append(line)
            continue
        parts = [p.strip() for p in SENT_RE.findall(line) if p.strip()]
        buf = ""
        for part in parts:
            candidate = (buf + " " + part).strip()
            if buf and syl(candidate) / sps > MAX_BEAT:
                beats.append(buf)
                buf = part
            else:
                buf = candidate
        if buf:
            beats.append(buf)
    return beats


def analyse(raw, sps=DEFAULT_SPS, target=None):
    beats = split_beats(raw, sps)
    if not beats:
        return None

    rows, clock = [], 0.0
    for i, text in enumerate(beats):
        s = syl(text)
        dur = s / sps
        rows.append({
            "n": i + 1, "start": round(clock, 2), "dur": round(dur, 2),
            "words": len(words(text)), "syllables": s, "text": text,
            "concrete": concrete_count(text), "label": "", "flags": [],
        })
        clock += dur
    total = clock

    for r in rows:
        if r["n"] == 1 or r["start"] + r["dur"] <= HOOK_WINDOW:
            r["label"] = "HOOK"
    rows[-1]["label"] = "CTA" if rows[-1]["label"] != "HOOK" else "HOOK/CTA"
    half = total / 2
    for r in rows:
        if not r["label"] and r["start"] <= half < r["start"] + r["dur"]:
            r["label"] = "TENGAH"

    notes = []
    if rows[0]["dur"] > HOOK_WINDOW:
        rows[0]["flags"].append(f"hook {rows[0]['dur']:.1f} dtk, lewat batas {HOOK_WINDOW:g} dtk")
        notes.append(f"Beat 1 butuh {rows[0]['dur']:.1f} dtk untuk diucapkan. Pangkas jadi "
                     f"{int(HOOK_WINDOW * sps)} suku kata atau kurang, atau hook-nya baru "
                     "mendarat setelah penonton memutuskan.")
    if rows[0]["concrete"] == 0:
        notes.append("Beat 1 tidak punya angka atau nama. Hook tanpa sesuatu yang bisa "
                     "dicek adalah hook yang di-scroll.")

    for r in rows:
        if r["dur"] > MAX_BEAT:
            r["flags"].append(f"{r['dur']:.1f} dtk di satu beat")
    long_beats = [r["n"] for r in rows if r["dur"] > MAX_BEAT]
    if long_beats:
        notes.append(f"Beat {', '.join(map(str, long_beats))} lebih dari {MAX_BEAT:g} dtk. "
                     "Pecah kalimatnya atau ganti visual di tengahnya. Frame diam adalah "
                     "tempat orang pergi.")

    run, start = 0, None
    for r in rows:
        if r["concrete"] == 0:
            run += 1
            start = start if start is not None else r["n"]
            if run == ABSTRACT_RUN:
                notes.append(f"Beat {start}-{r['n']} tidak punya hal konkret. Taruh angka, "
                             "nama, atau harga di salah satunya.")
        else:
            run, start = 0, None

    def content(text):
        return {w.lower() for w in words(text) if w.lower() not in STOPWORDS and len(w) > 2}

    loop = sorted(pretty(w) for w in content(rows[0]["text"]) & content(rows[-1]["text"]))
    if loop:
        notes.append(f"Loop: beat terakhir mengulang \"{', '.join(loop[:3])}\" dari hook. "
                     "Tontonan kedua itu jangkauan gratis.")
    else:
        notes.append("Tidak ada loop. Beat terakhir tidak berbagi kata dengan hook, jadi videonya "
                     "berakhir datar. Mengulang satu kata dari beat 1 adalah replay paling murah.")

    if target:
        delta = total - target
        if abs(delta) <= target * 0.1:
            notes.append(f"Durasi pas target ({total:.1f} dtk dari {target:g} dtk).")
        elif delta > 0:
            notes.append(f"{delta:.1f} dtk lebih dari target. Potong sekitar "
                         f"{int(delta * sps)} suku kata (kira-kira {max(1, int(delta * sps / 2.6))} kata).")
        else:
            notes.append(f"{-delta:.1f} dtk kurang dari target. Tambah sekitar "
                         f"{int(-delta * sps / 2.6)} kata, atau rekam versi pendek. "
                         "Versi pendek biasanya yang benar.")

    return {
        "sps": sps, "target": target,
        "total_seconds": round(total, 2),
        "total_words": sum(r["words"] for r in rows),
        "total_syllables": sum(r["syllables"] for r in rows),
        "beats": rows, "notes": notes,
    }


def render(a, out=sys.stdout):
    head = (f"BEAT SHEET  ·  {a['total_words']} kata / {a['total_syllables']} suku kata  ·  "
            f"~{a['total_seconds']:.1f} dtk di {a['sps']:g} suku kata/dtk"
            + (f"  ·  target {a['target']:g} dtk" if a["target"] else ""))
    print("\n" + head, file=out)
    print("=" * max(len(head), 72), file=out)
    for r in a["beats"]:
        label = f"{r['label']:<8}" if r["label"] else " " * 8
        print(f"  {tc(r['start'])}  {r['dur']:4.1f}s  {label}{r['text']}", file=out)
        for f in r["flags"]:
            print(f"  {'':>6}  {'':>5}  {'':<8}^ {f}", file=out)
    print("-" * max(len(head), 72), file=out)
    for n in a["notes"]:
        print(f"  - {n}", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Hitung waktu naskah Reel jadi beat sheet.")
    ap.add_argument("input", nargs="?", default="-", help="file naskah, atau - untuk stdin")
    ap.add_argument("--sps", type=float, default=DEFAULT_SPS,
                    help=f"laju bicara, suku kata per detik (default {DEFAULT_SPS})")
    ap.add_argument("--target", type=float, help="target durasi dalam detik")
    ap.add_argument("--kalibrasi", type=float, metavar="DETIK",
                    help="durasi nyata saat kamu membaca naskah ini; mencetak laju bicaramu")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    if args.kalibrasi:
        total = syl(normalize_numbers(raw))
        rate = total / args.kalibrasi
        print(f"{total} suku kata dalam {args.kalibrasi:g} dtk = {rate:.1f} suku kata/detik.\n"
              f"Simpan di voice.md (bagian Tempo) dan pakai: --sps {rate:.1f}")
        return
    a = analyse(raw, sps=args.sps, target=args.target)
    if not a:
        print("naskah kosong", file=sys.stderr)
        sys.exit(2)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)


if __name__ == "__main__":
    main()
