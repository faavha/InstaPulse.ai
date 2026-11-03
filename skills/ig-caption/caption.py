#!/usr/bin/env python3
"""
caption.py - periksa caption Instagram dan tunjukkan persis apa yang tampil di
feed sebelum "... selengkapnya".

Instagram memberi caption sekitar 125 karakter di feed dan menyembunyikan
sisanya di balik ketukan. Hampir semua caption yang gagal, gagal di situ: hook
ada di kalimat ketiga, baris pertama berisi sapaan ("Halo sobat cuan!"), atau
dibuka dengan hashtag. Script ini mencetak jendela yang terlihat sebagai kotak
supaya kamu membacanya seperti orang asing yang sedang scroll, lalu memeriksa
hal-hal yang memang layak diperiksa.

Angka 125 itu perkiraan. Angka sebenarnya bergeser tergantung HP, ukuran font
dan letak baris baru, makanya lebih baik punya ruang cadangan daripada caption
yang direkayasa pas berhenti di 125. Ubah dengan --truncate.

Versi bahasa Indonesia: mengenali ajakan (CTA) bahasa Indonesia ("komen MAU",
"cek link di bio", "simpan dulu"), hashtag generik lokal (#fypシ, #viralindonesia),
format rupiah, dan sapaan pembuka di baris pertama.

Pemakaian
  python3 caption.py caption.txt
  python3 caption.py caption.txt --keywords "jasa desain logo,logo umkm"
  python3 caption.py caption.txt --json
"""

import argparse
import json
import re
import sys
import textwrap

LIMIT = 2200             # batas keras caption Instagram.
TRUNCATE = 125           # kira-kira di mana feed memotong jadi "... selengkapnya".
HASHTAG_LIMIT = 5        # batas per post/Reel sejak 18 Des 2025 (sebelumnya 30),
                         # diumumkan akun @creators Instagram.

HASHTAG_RE = re.compile(r"(?:^|\s)(#[^\s#]+)")
MENTION_RE = re.compile(r"(?:^|\s)(@[A-Za-z0-9_.]+)")
LINK_RE = re.compile(r"https?://\S+|\bwww\.\S+|\bwa\.me/\S+|\bbit\.ly/\S+|\bs\.id/\S+"
                     r"|\b[a-z0-9-]+\.(?:com|co\.id|co|id|io|net|org|ai|app|my\.id|biz\.id)/\S*",
                     re.IGNORECASE)
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿←-⇿]")
CONCRETE_RE = re.compile(r"(?i:rp\.?\s?|\$\s?)\d|\b\d[\d,.]*|(?<!^)(?<![.!?]\s)\b[A-Z][a-z]{2,}\b"
                         r"|\b[A-Z]{2,6}\b", re.MULTILINE)

ASKS = [
    (re.compile(r"(?i)\b(?:komen|komentar|ketik|tulis|comment)\s+(?:kata\s+)?[\"'“]?[A-Z0-9]{2,}\b"),
     "komen kata kunci"),
    (re.compile(r"(?i)\b(?:dm|chat|wa|whatsapp|kirim pesan|message)\s+(?:aku|saya|kami|admin|kita|me)\b"),
     "DM / chat"),
    (re.compile(r"(?i)\b(?:simpan|save)\b(?:\s+(?:dulu|ini|postingan|post|reels?|biar|this|it))?"),
     "simpan"),
    (re.compile(r"(?i)\b(?:share|bagikan|kirim(?:kan)?)\b\s+(?:ke|ini|this|it|postingan)"),
     "share / kirim ke teman"),
    (re.compile(r"(?i)\b(?:follow|ikuti)\s+(?:aku|saya|kami|akun|@|me|for)"),
     "follow"),
    (re.compile(r"(?i)\b(?:link|tautan)(?:\s+[\w-]+){0,3}\s+(?:ada\s+)?(?:di|in)\s+(?:my\s+)?bio\b|\bcek bio\b|\bklik link\b"),
     "link di bio"),
    (re.compile(r"(?i)\b(?:geser|swipe|tap)\b\s*(?:ke|untuk|buat|left|right|for|to|through)?"),
     "geser / swipe"),
    (re.compile(r"(?i)\b(?:menurut (?:kamu|kalian)|kasih tau|tim mana|pilih mana|"
                r"kalian lebih|which one|tell me)\b"),
     "jawab pertanyaan"),
    (re.compile(r"(?i)\b(?:tag|mention)\s+(?:teman|temen|bestie|pasangan|someone)\b"),
     "tag teman"),
]

# Hashtag yang tidak mendeskripsikan apa pun.
FILLER_RE = re.compile(
    r"(?i)^#(?:fyp\w*|foryou\w*|viral\w*|explore\w*|trending\w*|reels\w*|instagood|"
    r"instadaily|love|follow\w*|like4like|likeforlike|l4l|f4f|instagram\w*|"
    r"beranda\w*|masukberanda|berandaig|tiktok\w*|xyzbca|zyxcba|ig|igers\w*)$")

GREETING_RE = re.compile(
    r"(?i)^\s*(?:hal+o|hai|hay|helo|hi\b|hey\b|assalamu'?\s?alaikum|selamat (?:pagi|siang|sore|malam)|"
    r"apa kabar|guys|gaes|sobat|teman-teman|temen-temen|bestie|dear\b)")


def visible_window(text, cut):
    """Yang tampil di feed. Instagram memotong di tengah kata, script ini juga."""
    flat = text.strip()
    return flat if len(flat) <= cut else flat[:cut]


def render_box(window, truncated, out=sys.stdout, width=52):
    print("\n  YANG TAMPIL DI FEED", file=out)
    print("  +" + "-" * (width + 2) + "+", file=out)
    lines = []
    for raw in window.split("\n"):
        lines.extend(textwrap.wrap(raw, width) or [""])
    for line in lines[:8]:
        print(f"  | {line:<{width}} |", file=out)
    tail = "... selengkapnya" if truncated else "(caption muat semua)"
    print("  +" + "-" * (width + 2 - len(tail) - 2) + f" {tail} " + "+", file=out)


def analyse(text, cut=TRUNCATE, keywords=None):
    stripped = text.strip()
    chars = len(stripped)
    lines = stripped.split("\n")
    first_line = lines[0].strip() if lines else ""
    tags = HASHTAG_RE.findall(stripped)
    mentions = MENTION_RE.findall(stripped)
    links = LINK_RE.findall(stripped)
    emoji = EMOJI_RE.findall(stripped)
    window = visible_window(stripped, cut)
    truncated = chars > cut
    asks = [name for pattern, name in ASKS if pattern.search(stripped)]
    filler = [t for t in tags if FILLER_RE.match(t)]
    keywords = [k.strip() for k in (keywords or []) if k.strip()]

    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    add("PANJANG", "GAGAL" if chars > LIMIT else "LULUS",
        f"{chars} / {LIMIT} karakter" + (f", lebih {chars - LIMIT}" if chars > LIMIT else ""))

    if not first_line:
        add("BARIS PERTAMA", "GAGAL", "caption dibuka dengan baris kosong")
    elif first_line.startswith(("#", "@")):
        add("BARIS PERTAMA", "GAGAL",
            "dibuka dengan hashtag atau mention, padahal itu satu-satunya posisi yang layak diisi kalimat")
    elif GREETING_RE.search(first_line):
        add("BARIS PERTAMA", "GAGAL",
            "dibuka dengan sapaan. Orang asing di feed tidak datang untuk disapa; "
            "pindahkan salam ke bawah atau hapus")
    elif len(first_line) > cut:
        add("BARIS PERTAMA", "PERIKSA",
            f"{len(first_line)} karakter, jadi terpotong di {cut} di tengah pikiran. "
            "Oke kalau potongannya bikin penasaran, buruk kalau di tengah anak kalimat")
    else:
        add("BARIS PERTAMA", "LULUS", f"{len(first_line)} karakter, tampil utuh")

    n_concrete = len(CONCRETE_RE.findall(window))
    add("HOOK KONKRET", "LULUS" if n_concrete else "PERIKSA",
        f"{n_concrete} angka/nama di jendela yang terlihat"
        + ("" if n_concrete else " - tidak ada yang bisa dicek sebelum diketuk"))

    if len(tags) > HASHTAG_LIMIT:
        add("HASHTAG", "GAGAL", f"{len(tags)} tag, lewat batas Instagram {HASHTAG_LIMIT}. "
                                "Kelebihannya tidak dihitung dan bloknya kelihatan jadul"
                                + (f". Buang yang generik dulu: {', '.join(filler[:3])}" if filler else ""))
    elif filler:
        add("HASHTAG", "PERIKSA", f"{len(tags)} tag, {len(filler)} di antaranya generik "
                                  f"({', '.join(filler[:3])}). Itu tidak mendeskripsikan apa-apa; "
                                  "pakai slotnya untuk topik")
    else:
        add("HASHTAG", "LULUS", f"{len(tags)} tag" + (f": {' '.join(tags)}" if tags else ""))

    if not tags:
        add("LETAK TAG", "LULUS", "tidak ada tag")
    elif any(t in window for t in tags):
        add("LETAK TAG", "PERIKSA", "ada hashtag di jendela yang terlihat, "
                                    "ruang feed terpakai untuk label")
    else:
        add("LETAK TAG", "LULUS", "tag ada di bawah lipatan")

    add("LINK", "PERIKSA" if links else "LULUS",
        f"{len(links)} link di caption, padahal link di caption tidak bisa diklik. "
        "Pindahkan ke bio, story link, atau kirim lewat DM" if links else "tidak ada link mati")

    if len(asks) == 1:
        add("SATU AJAKAN", "LULUS", f"satu CTA: {asks[0]}")
    elif not asks:
        add("SATU AJAKAN", "PERIKSA", "tidak ada CTA. Putuskan post ini untuk apa")
    else:
        add("SATU AJAKAN", "PERIKSA", f"{len(asks)} ajakan ({', '.join(asks)}). "
                                      "Dua ajakan sama saja dengan tidak ada")

    density = len(emoji) * 100 / max(chars, 1)
    add("EMOJI", "PERIKSA" if density > 4 else "LULUS",
        f"{len(emoji)} emoji, {density:.1f} per 100 karakter"
        + (" - terbaca sebagai hiasan" if density > 4 else ""))

    if keywords:
        low = stripped.lower()
        found = [k for k in keywords if k.lower() in low]
        missing = [k for k in keywords if k.lower() not in low]
        in_window = [k for k in found if k.lower() in window.lower()]
        status = "LULUS" if not missing else ("PERIKSA" if found else "GAGAL")
        add("KATA PENCARIAN", status,
            f"{len(found)}/{len(keywords)} ada"
            + (f", {len(in_window)} di jendela yang terlihat" if found else "")
            + (f". Belum ada: {', '.join(missing)}" if missing else ""))

    fails = sum(1 for c in checks if c["status"] == "GAGAL")
    warns = sum(1 for c in checks if c["status"] == "PERIKSA")
    verdict = "PERBAIKI" if fails else ("TINJAU" if warns else "SIAP")

    return {
        "characters": chars, "limit": LIMIT, "truncate_at": cut,
        "visible": window, "truncated": truncated,
        "first_line_chars": len(first_line),
        "hashtags": tags, "mentions": mentions, "links": links,
        "emoji": len(emoji), "asks": asks,
        "checks": checks, "verdict": verdict,
    }


def render(a, out=sys.stdout):
    head = (f"CEK CAPTION  ·  {a['characters']} / {a['limit']} karakter  ·  "
            f"{len(a['hashtags'])} hashtag  ·  {len(a['asks'])} ajakan")
    print("\n" + head, file=out)
    print("=" * max(len(head), 62), file=out)
    render_box(a["visible"], a["truncated"], out=out)
    print("", file=out)
    for c in a["checks"]:
        print(f"  {c['status']:<7} {c['check']:<15} {c['detail']}", file=out)
    print("-" * max(len(head), 62), file=out)
    print(f"  HASIL  {a['verdict']}\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Periksa caption Instagram.")
    ap.add_argument("input", nargs="?", default="-", help="file caption, atau - untuk stdin")
    ap.add_argument("--truncate", type=int, default=TRUNCATE,
                    help=f"karakter yang tampil sebelum '... selengkapnya' (default {TRUNCATE})")
    ap.add_argument("--keywords", default="", help="kata pencarian, pisahkan dengan koma")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, cut=args.truncate, keywords=args.keywords.split(","))
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0 if a["verdict"] == "SIAP" else 1)


if __name__ == "__main__":
    main()
