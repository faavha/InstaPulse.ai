#!/usr/bin/env python3
"""
hookscore.py - beri skor kalimat pertama Reel pada lima hal yang dimiliki
hook kuat, lalu urutkan beberapa hook sekaligus.

Versi bahasa Indonesia. Bekerja untuk hook Indonesia, Inggris, maupun campuran
("Gaji UMR tapi bisa invest 2 juta sebulan? Ini caranya.").

Apa ini:  lima heuristik lokal, dihitung di komputer kamu dari teks saja.
Yang diukur adalah sifat yang biasanya dimiliki hook yang menahan perhatian:
panjang yang bisa diucapkan dalam 3,5 detik, ada penanda konkret (angka,
nama, harga), ada yang dipertaruhkan, isi pentingnya di depan, dan jelas
ditujukan ke siapa.

Apa ini BUKAN:  peramal views. Versi asli bahasa Inggrisnya diuji pada 74 hook
nyata: bagus untuk membedakan hook asli dari hook yang sengaja dibuat jelek
(AUC 0,83), hampir tidak bisa membedakan video sukses dan gagal dari kreator
yang sama (AUC 0,56, nyaris lempar koin). Daftar kata Indonesia di versi ini
belum diuji ulang pada data Indonesia, jadi anggap ini checklist, bukan ramalan.

Gunakan untuk yang memang bisa diukurnya: menangkap sapaan ("Halo guys"),
pembukaan basa-basi ("Di video kali ini..."), hook tanpa angka atau nama, dan
hook yang butuh lima detik untuk diucapkan. Mana dari dua hook bagus yang akan
meledak ditentukan wajahmu, editanmu, audiomu dan kepada siapa Instagram
menampilkannya. Percayai grafik retensi, bukan script ini.

Panjang dihitung dalam SUKU KATA, bukan kata (lihat idlang.py).

Pemakaian
  python3 hookscore.py hooks.txt              # satu hook per baris, diurutkan
  python3 hookscore.py --hook "Rp18 juta hilang gara-gara satu pasal kontrak."
  python3 hookscore.py hooks.txt --sps 6.2    # laju bicaramu sendiri
  python3 hookscore.py hooks.txt --json
"""

import argparse
import json
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from idlang import (MONEY_WORDS, SPOKEN_NUMBERS, STAKES, is_first_person,  # noqa: E402
                    is_second_person, normalize_numbers, syllables_word, words)

DEFAULT_SPS = 5.5        # suku kata per detik, bicara santai ke kamera

NUMBER_RE = re.compile(r"(?:rp\.?\s?|\$\s?)?\d[\d.,]*\s?(?:%|k\b|rb\b|jt\b|x\b)?", re.IGNORECASE)
PROPER_RE = re.compile(r"(?<!^)(?<![.!?]\s)\b[A-Z][a-z]{2,}\b")
ACRONYM_RE = re.compile(r"\b[A-Z]{2,6}\b")
HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")

# Pembuka yang menghabiskan detik pertama tanpa isi.
WEAK_OPENERS = [
    # Indonesia
    "halo", "hallo", "helo", "hai", "hay", "guys", "gaes", "gais", "gengs", "geng",
    "teman", "temen", "sobat", "assalamualaikum", "assalamu'alaikum", "selamat",
    "oke", "ok", "okay", "jadi", "nah", "gini", "begini", "kali ini", "hari ini",
    "di video", "pada video", "dalam video", "video ini", "di reels", "aku mau",
    "saya mau", "gue mau", "gw mau", "aku akan", "saya akan", "kali ini",
    "kalian tahu", "kalian tau", "tau gak", "tau nggak", "tahu nggak", "tahu gak",
    "pernah gak", "pernah nggak", "apakah kamu", "apakah kalian", "kalian pernah",
    "sebenarnya", "sebenernya", "langsung aja", "yuk", "mari", "ini adalah",
    "seperti yang", "jujur aja", "btw", "eh",
    # Inggris
    "so", "hey", "hi", "hello", "yo", "alright", "welcome", "today", "basically",
    "honestly", "look", "listen", "um", "just", "let", "lets", "let's",
    "i wanted", "i want", "have you", "did you", "do you", "are you", "in this",
    "in today", "this is", "it is", "you know",
]

# Kata perintah yang pantas berada di depan.
IMPERATIVES = {
    "stop", "berhenti", "jangan", "coba", "simpan", "save", "pakai", "pake",
    "tiru", "contek", "curi", "hapus", "tonton", "lihat", "liat", "cek",
    "mulai", "bikin", "buat", "tulis", "kirim", "ambil", "catat", "ganti",
    "hindari", "tinggalkan", "matikan", "nyalakan", "pasang", "beli", "jual",
    "steal", "copy", "delete", "try", "watch", "read", "use", "build", "make",
    "write", "send", "take", "start", "quit", "never", "always", "don't", "check",
}

GREETING_RE = re.compile(
    r"(?i)^\s*(?:hal+o|hai|hay|helo|hey|hi\b|yo\b|guys|gaes|gais|"
    r"assalamu'?\s?alaikum|selamat (?:pagi|siang|sore|malam)|apa kabar|"
    r"welcome|what'?s up|sobat\b|teman-teman|temen-temen)")

DEALBREAKERS = [
    (re.compile(r"(?i)^\s*(?:stop scroll\w*|jangan (?:di)?-?scroll\w*|jangan (?:di)?-?skip|"
                r"tunggu,? jangan|don'?t scroll)"),
     "Dibuka dengan \"jangan scroll\". Minta perhatian justru membuktikan kamu belum layak dapat."),
    (re.compile(r"(?i)\b(?:(?:di|pada|dalam) (?:video|reels?|konten|postingan) "
                r"(?:ini|kali ini|hari ini)|aku (?:mau|akan) (?:kasih tau|nunjukin|bahas|share|sharing)|"
                r"saya (?:akan|mau|ingin) (?:menunjukkan|membahas|berbagi)|"
                r"gue (?:mau|bakal) (?:bahas|kasih tau|nunjukin)|"
                r"in (?:this|today'?s) (?:video|reel)|i'?m going to show you)\b"),
     "Basa-basi pembuka video. Hapus, langsung buka dengan inti/hasilnya."),
    (GREETING_RE,
     "Sapaan. Salam boleh, tapi taruh SETELAH hook. Detik pertama milik hook."),
    (re.compile(r"(?i)\btonton (?:sampai|sampe) (?:habis|abis|akhir|selesai)\b|\bwatch till the end\b"),
     "\"Tonton sampai habis\". Janji yang belum ditepati bukan alasan untuk bertahan."),
    (HASHTAG_RE,
     "Hashtag di hook. Hashtag tempatnya di bawah caption, kalau perlu."),
    (EMOJI_RE,
     "Emoji di hook. Teks layar ukuran hook cuma muat kata atau emoji, bukan dua-duanya."),
]


def clamp(n):
    return max(0.0, min(100.0, n))


def low_words(text):
    return [w.lower().strip("'’") for w in words(text)]


def check_length(text, sps=DEFAULT_SPS):
    """Hook harus mendarat sebelum jempol bergerak. Paling lama 3,5 detik.

    Batasnya sama dengan HOOK_WINDOW di beats.py, supaya dua alat ini tidak
    saling bertentangan. Di bawah 8 suku kata biasanya terlalu tipis untuk
    membawa angka dan taruhan sekaligus.
    """
    w = words(text)
    syl = sum(syllables_word(x) for x in w)
    secs = syl / sps
    chars = len(text.strip())
    lo, hi = 8, int(round(3.5 * sps))        # 8 s.d. 19 suku kata di 5,5/detik
    if lo <= syl <= hi:
        score = 100.0
    elif syl < lo:
        score = clamp(100 - (lo - syl) * 12)
    else:
        score = clamp(100 - (syl - hi) * 7)
    if chars > 60:                       # dua baris teks layar ukuran besar
        score -= 12
    return clamp(score), (f"{len(w)} kata, {syl} suku kata, {chars} karakter, "
                          f"~{secs:.1f} dtk diucapkan (ideal {lo}-{hi} suku kata)")


def check_specificity(text):
    """Satu hal konkret mengalahkan tiga hal abstrak."""
    norm = normalize_numbers(text)
    nums = [n.strip() for n in NUMBER_RE.findall(norm) if re.search(r"\d", n)]
    propers = set(PROPER_RE.findall(text)) | set(ACRONYM_RE.findall(text))
    low = low_words(text)
    spoken = [w for w in low if w in SPOKEN_NUMBERS or w in MONEY_WORDS]
    hits = len(nums) + len(propers) + len(spoken)
    score = 15.0 if hits == 0 else clamp(45 + hits * 30)
    found = ", ".join(nums[:2] + sorted(propers)[:2] + spoken[:2])
    return score, (f"{hits} penanda konkret" + (f": {found}" if found else
                   " - tidak ada angka, nama, atau apa pun yang bisa dicek"))


def check_stakes(text):
    """Ketegangan, biaya, penyangkalan. Sesuatu yang bisa hilang dari penonton."""
    hits = [x for x in low_words(text) if x in STAKES]
    markers = sorted(set(hits))
    if re.search(r"(?i)(?:rp\.?\s?|\$\s?)\d", text):
        markers.append("harga")
    n = len(markers)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    detail = f"{n} penanda taruhan" + (f": {', '.join(markers[:4])}" if markers else
                                       " - tidak ada yang dipertaruhkan di kalimat ini")
    return clamp(score), detail


def check_frontload(text):
    """Kata yang menarik tidak boleh ada di posisi kesembilan."""
    w = words(text)
    if not w:
        return 0.0, "kosong"
    low = [x.lower().strip("'’") for x in w]
    opener = " ".join(low[:2])
    penalty, hit_opener = 0, None
    for weak in WEAK_OPENERS:
        if opener == weak or opener.startswith(weak + " ") or low[0] == weak:
            penalty, hit_opener = 30, weak
            break
    payload = None
    for i, token in enumerate(low):
        if (token in STAKES or token in SPOKEN_NUMBERS or token in MONEY_WORDS
                or re.search(r"\d", token) or (i and PROPER_RE.match(w[i]))
                or ACRONYM_RE.fullmatch(w[i])):
            payload = i
            break
    if payload is None:
        base, where = 30.0, "tidak ada kata isi di seluruh kalimat"
    elif payload <= 3:
        base, where = 100.0, f"isi di kata ke-{payload + 1}"
    elif payload <= 6:
        base, where = 70.0, f"isi di kata ke-{payload + 1}, bisa dimajukan"
    else:
        base, where = 40.0, f"isi di kata ke-{payload + 1}, terlambat"
    detail = where + (f"; pembuka lemah \"{hit_opener}\"" if hit_opener else "")
    return clamp(base - penalty), detail


def check_address(text):
    """Ditujukan ke satu penonton, atau melayang di udara."""
    w = words(text)
    low = [x.lower() for x in w]
    second = [x for x in w if is_second_person(x)]
    if second:
        return 100.0, f"bicara ke penonton (\"{second[0]}\")"
    if low and low[0] in IMPERATIVES:
        return 90.0, f"dibuka kalimat perintah (\"{low[0]}\")"
    if any(is_first_person(x) for x in w):
        return 70.0, "orang pertama, penonton tidak disebut"
    return 35.0, "orang ketiga, tidak ada siapa-siapa di ruangan"


CHECKS = ["PANJANG", "KONKRET", "TARUHAN", "DI DEPAN", "SAPAAN KE"]


def run(text, sps=DEFAULT_SPS):
    results = {
        "PANJANG": check_length(text, sps),
        "KONKRET": check_specificity(text),
        "TARUHAN": check_stakes(text),
        "DI DEPAN": check_frontload(text),
        "SAPAAN KE": check_address(text),
    }
    flags = [msg for pattern, msg in DEALBREAKERS if pattern.search(text)]
    scores = [results[c][0] for c in CHECKS]
    # Sifat terlemah membatasi hook: satu kelemahan cukup bikin jempol lanjut.
    overall = clamp(statistics.mean(scores) * 0.6 + min(scores) * 0.4 - len(flags) * 15)
    verdict = "KUAT" if overall >= 70 and min(scores) >= 55 and not flags else (
        "OKE" if overall >= 50 else "LEMAH")
    return results, overall, verdict, flags


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render_one(text, results, overall, verdict, flags, out=sys.stdout):
    print("\nSKOR HOOK", file=out)
    print("=" * 62, file=out)
    print(f"  \"{text.strip()}\"\n", file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<10} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<10} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'TOTAL':<10} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    for f in flags:
        print(f"\n  FATAL  {f}", file=out)
    if verdict != "KUAT":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Sifat terlemah: {weakest}. Perbaiki itu dulu, lalu jalankan lagi.", file=out)
    print("", file=out)


def render_table(rows, out=sys.stdout):
    print("\nPERINGKAT HOOK\n" + "=" * 78, file=out)
    for i, r in enumerate(rows, 1):
        mark = "->" if i == 1 else "  "
        hook = r["hook"] if len(r["hook"]) <= 62 else r["hook"][:59] + "..."
        print(f"{mark} {r['score']:5.1f} {r['verdict']:<6} {hook}", file=out)
        print(f"        terlemah: {r['weakest']} ({r['checks'][r['weakest']]['score']:.0f})", file=out)
        for f in r["flags"]:
            print(f"        fatal: {f}", file=out)
    print("\nRekam yang teratas. Kalau yang teratas di bawah 50, belum ada yang layak jadi hook.\n",
          file=out)


def main():
    ap = argparse.ArgumentParser(description="Skor hook Reel pada lima sifat.")
    ap.add_argument("input", nargs="?", default="-", help="file berisi satu hook per baris, atau -")
    ap.add_argument("--hook", help="skor satu hook langsung dari command line")
    ap.add_argument("--sps", type=float, default=DEFAULT_SPS,
                    help=f"laju bicara, suku kata per detik (default {DEFAULT_SPS})")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.hook:
        lines = [args.hook]
    else:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    if not lines:
        print("tidak ada yang bisa diskor", file=sys.stderr)
        sys.exit(2)

    payload = []
    for line in lines:
        results, overall, verdict, flags = run(line, args.sps)
        payload.append({
            "hook": line,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "weakest": min(CHECKS, key=lambda c: results[c][0]),
            "flags": flags,
            "score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if len(payload) > 1 else payload[0], indent=2, ensure_ascii=False))
        return
    if len(payload) == 1:
        render_one(lines[0], *run(lines[0], args.sps))
    else:
        render_table(sorted(payload, key=lambda r: -r["score"]))
    sys.exit(0 if max(p["score"] for p in payload) >= 70 else 1)


if __name__ == "__main__":
    main()
