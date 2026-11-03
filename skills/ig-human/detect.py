#!/usr/bin/env python3
"""
detect.py - panel lima pemeriksaan yang menilai seberapa "mesin" sebuah draf.

Apa ini:  lima heuristik lokal yang meniru sinyal yang diukur detektor AI
publik: variasi panjang kalimat, kekonkretan, kosakata klise, sidik jari
tipografi, dan suara (voice). Semua dihitung di komputer kamu dari teks saja.
Tidak ada yang diunggah.

Apa ini BUKAN:  GPTZero, Originality, Copyleaks, Winston atau Turnitin. Script
ini tidak memanggil API mereka dan tidak bisa menjanjikan vonis mereka.

Versi bahasa Indonesia: pemeriksaan VOICE tidak lagi mencari kontraksi
bahasa Inggris (don't, it's), tapi penanda bahasa lisan Indonesia (nggak,
udah, aja, sih, dong, kok, banget, gimana) dan menghukum penanda register kaku
hasil terjemahan (Anda, merupakan, tersebut, sebuah, memiliki) kalau
registermu santai. Pakai --register formal untuk akun institusi.

Setiap pemeriksaan memberi skor MANUSIA 0 sampai 100. Makin tinggi makin baik.

Pemakaian
  python3 detect.py draf.txt
  python3 detect.py draf.txt --register formal
  python3 detect.py draf.txt --json
  python3 detect.py sebelum.txt sesudah.txt      # bandingkan dua draf
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
WORD_RE = re.compile(r"[A-Za-z']+")
CONTRACTIONS = re.compile(r"\b\w+'(?:s|t|re|ve|ll|d|m)\b", re.IGNORECASE)
PRONOUNS = re.compile(r"\b(i|me|my|mine|we|us|our|you|your|aku|saya|gue|gua|gw|ane|kami|kita|"
                      r"kamu|kalian|lo|lu|elo|elu|anda|kak|bestie)\b", re.IGNORECASE)
NUMBERS = re.compile(r"\b\d[\d,.]*%?\b|\$\d|(?i:rp)\.?\s?\d")
EMOJI_SEQ_RE = re.compile(
    r"[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF][\uFE0F\U0001F3FB-\U0001F3FF]*"
    r"(?:\u200D[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF][\uFE0F\U0001F3FB-\U0001F3FF]*)+"
    r"|\U0001F3F4[\U000E0020-\U000E007E]+\U000E007F")
PROPER = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-Z][a-z]{2,}\b", re.MULTILINE)


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    """Map value onto 0-100 where `human` -> 100 and `machine` -> 0."""
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


QUOTE_RE = re.compile(r'["“][^"”\n]{1,80}["”]')


def mask_quotes(text):
    """Kutipan pendek biasanya contoh, bukan suara penulis."""
    return QUOTE_RE.sub('"kutipan"', text)


def sentences(text):
    # "Rp5.000" dan "4,5 juta" bukan akhir kalimat.
    text = re.sub(r"(?<=\d)[.,](?=\d)", "", text)
    return [s.strip() for s in SENT_RE.findall(text) if len(s.split()) >= 1]


def words(text):
    return WORD_RE.findall(text)


def check_burstiness(text):
    """Humans vary sentence length hard. Models write even."""
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return 50.0, "terlalu pendek untuk dinilai"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    score = scale(cv, human=0.70, machine=0.22)
    return score, f"variasi {cv:.2f} dari {len(lens)} kalimat (ideal 0,55+)"


def check_specificity(text):
    """Numbers, names and concrete nouns. Slop is abstract."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "terlalu pendek untuk dinilai"
    per100 = 100 / len(w)
    hits = len(NUMBERS.findall(text)) + len(set(PROPER.findall(text)))
    density = hits * per100
    score = scale(density, human=6.0, machine=0.5)
    return score, f"{hits} penanda konkret, {density:.1f} per 100 kata (ideal 4+)"


def check_slop(text, lex):
    """Stock vocabulary density against the lexicon."""
    w = words(text)
    if not w:
        return 50.0, "kosong"
    hits, found = 0, []
    for entry in lex["words"] + lex["phrases"]:
        pattern = re.compile(r"\b" + re.escape(entry["find"]).replace(r"\ ", r"\s+") + r"\b",
                             re.IGNORECASE)
        n = len(pattern.findall(text))
        if n:
            hits += n
            found.append(entry["find"])
    density = hits * 100 / len(w)
    score = scale(density, human=0.0, machine=4.0)
    detail = f"{hits} istilah klise, {density:.1f} per 100 kata"
    if found:
        detail += " (" + ", ".join(sorted(found)[:4]) + (", ..." if len(found) > 4 else "") + ")"
    return score, detail


def check_fingerprint(text):
    """Characters a phone keyboard does not produce."""
    bare = EMOJI_SEQ_RE.sub("", text)      # ZWJ di dalam emoji gabungan itu sah
    invisible = sum(1 for c in bare if unicodedata.category(c) == "Cf")
    em = text.count("—")
    curly = sum(text.count(c) for c in "‘’“”")
    ellip = text.count("…")
    nbsp = sum(text.count(c) for c in "   ")
    total = invisible * 4 + em * 2 + curly + ellip + nbsp
    per1k = total * 1000 / max(len(text), 1)
    score = scale(per1k, human=0.0, machine=12.0)
    detail = (f"{invisible} tak terlihat, {em} em dash, {curly} kutip melengkung, "
              f"{ellip} elipsis, {nbsp} spasi keras")
    return score, detail


def _per100(markers, text, n_words):
    low = text.lower()
    hits = 0
    for m in markers:
        hits += len(re.findall(r"\b" + re.escape(m).replace(r"\ ", r"\s+") + r"\b", low))
    return hits * 100 / max(n_words, 1)


def check_voice(text, lex, register="santai"):
    """Bahasa lisan, kata ganti orang, dan bentuk-bentuk kebiasaan mesin."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "terlalu pendek untuk dinilai"
    per100 = 100 / len(w)
    casual = (_per100(lex.get("casual_markers", []), text, len(w))
              + len(CONTRACTIONS.findall(text)) * per100)
    formal = _per100(lex.get("formal_markers", []), text, len(w))
    person = len(PRONOUNS.findall(text)) * per100
    tells, names = 0, []
    for s in lex["structures"]:
        try:
            n = len(re.compile(s["regex"], re.MULTILINE).findall(text))
        except re.error:
            continue
        if n:
            tells += n
            names.append(s["id"])
    bullets = [len(b.split()) for b in re.findall(r"(?m)^\s*[-*•]\s+(.+)$", text)]
    uniform = (len(bullets) >= 3 and statistics.pstdev(bullets) < 1.6)
    tell_score = clamp(100 - tells * 22)
    person_score = scale(person, human=8.0, machine=1.0)
    if register == "formal":
        score = person_score * 0.45 + tell_score * 0.55
    else:
        score = (scale(casual, human=5.0, machine=0.0) * 0.35
                 + person_score * 0.35 + tell_score * 0.30)
        score -= min(30.0, formal * 6)       # "Anda", "merupakan", "tersebut" di akun santai
    if uniform:
        score -= 12
        names.append("bullet-seragam")
    detail = (f"{casual:.1f} penanda lisan, {formal:.1f} penanda kaku, {person:.1f} kata ganti "
              f"per 100 kata, {tells} pola struktural")
    if register == "formal":
        detail += " (register formal: penanda lisan/kaku tidak dihitung)"
    if names:
        detail += " [" + ", ".join(names[:4]) + "]"
    return clamp(score), detail


CHECKS = ["BURSTINESS", "SPECIFICITY", "SLOP DENSITY", "FINGERPRINT", "VOICE"]
# Nama tampilan Indonesia; kunci JSON tetap bahasa Inggris supaya stabil.
LABELS = {"BURSTINESS": "VARIASI", "SPECIFICITY": "KONKRET", "SLOP DENSITY": "KLISE",
          "FINGERPRINT": "SIDIK JARI", "VOICE": "SUARA"}


def run(text, lex, register="santai"):
    results = {}
    results["BURSTINESS"] = check_burstiness(text)
    results["SPECIFICITY"] = check_specificity(text)
    results["SLOP DENSITY"] = check_slop(mask_quotes(text), lex)
    results["FINGERPRINT"] = check_fingerprint(text)
    results["VOICE"] = check_voice(mask_quotes(text), lex, register)
    scores = [results[c][0] for c in CHECKS]
    # The weakest check drags the verdict: a detector only needs one signal.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    verdict = "LULUS" if overall >= 70 and min(scores) >= 55 else (
        "TINJAU" if overall >= 50 else "TERDETEKSI")
    return results, overall, verdict


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, label=None, out=sys.stdout):
    title = "PANEL DETEKSI AI" + (f"  -  {label}" if label else "")
    print("\n" + title, file=out)
    print("=" * max(len(title), 62), file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {LABELS[name]:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'SKOR MANUSIA':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    if verdict != "LULUS":
        weakest = LABELS[min(CHECKS, key=lambda c: results[c][0])]
        print(f"\n  Sinyal terlemah: {weakest}. Perbaiki itu dulu.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Nilai seberapa 'mesin' sebuah draf.")
    ap.add_argument("input", nargs="?", default="-", help="file, atau - untuk stdin")
    ap.add_argument("compare", nargs="?", help="file kedua, untuk sebelum/sesudah")
    ap.add_argument("--register", choices=["santai", "formal"], default="santai",
                    help="gaya bahasa akun (default santai)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lexicon", default=LEX)
    args = ap.parse_args()

    lex = json.load(open(args.lexicon, encoding="utf-8"))
    read = lambda p: sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()

    targets = [(args.input, read(args.input))]
    if args.compare:
        targets.append((args.compare, read(args.compare)))

    payload = []
    for name, text in targets:
        results, overall, verdict = run(text, lex, args.register)
        payload.append({
            "source": name,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "human_score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if args.compare else payload[0], indent=2, ensure_ascii=False))
        return

    for (name, text), p in zip(targets, payload):
        results, overall, verdict = run(text, lex, args.register)
        render(results, overall, verdict, label=os.path.basename(name) if args.compare else None)
    if args.compare:
        a, b = payload
        delta = b["human_score"] - a["human_score"]
        print(f"  {a['human_score']:.1f} {a['verdict']}  ->  "
              f"{b['human_score']:.1f} {b['verdict']}   ({delta:+.1f})\n")

    sys.exit(0 if payload[-1]["verdict"] == "LULUS" else 1)


if __name__ == "__main__":
    main()
