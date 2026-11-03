#!/usr/bin/env python3
"""
humanize.py - hapus sidik jari mesin dari sebuah draf (bahasa Indonesia,
Inggris, atau campuran).

Tiga tahap, berurutan:

  1. TAK TERLIHAT  hapus atau normalkan karakter yang tidak pernah dihasilkan
                   keyboard manusia: zero-width space, word joiner, soft hyphen,
                   BOM, karakter tag Unicode, spasi tak-putus dan spasi sempit.
                   Karakter ini ikut ter-copy-paste dan merupakan tanda paling
                   mekanis dari teks buatan mesin.
                   PENGECUALIAN: zero-width joiner di DALAM emoji gabungan
                   (👨‍💻, 👩‍👧, 🏳️‍🌈) dan karakter tag di dalam bendera (🏴󠁧󠁢󠁳󠁣󠁴󠁿) dipertahankan.
                   Versi aslinya menghapus semuanya, sehingga 👨‍💻 pecah jadi 👨💻.
  2. TIPOGRAFI     em dash -> koma, en dash -> tanda hubung, kutip melengkung ->
                   kutip lurus, elipsis -> tiga titik, bullet -> tanda hubung.
  3. LEKSIKON      ganti "bahasa AI" di slop.json dengan kata biasa, huruf
                   besar-kecil dipertahankan, URL tidak disentuh.

Pola struktural (pola tiga, "bukan sekadar X, tapi Y", tembok hashtag) hanya
DILAPORKAN, tidak ditulis ulang otomatis. Mengubah bentuk kalimat butuh
penilaian, jadi itu tugas model, bukan regex.

Pemakaian
  python3 humanize.py draft.txt
  python3 humanize.py draft.txt --report
  pbpaste | python3 humanize.py - --report
  python3 humanize.py draft.txt --json
  python3 humanize.py draft.txt -o clean.txt
"""

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+")
SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")


def load_lexicon(path=LEX):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _cp(spec):
    """'U+200B' -> '\\u200b';  'U+E0000-U+E007F' -> (start, end)."""
    if "-" in spec:
        a, b = spec.split("-")
        return (int(a[2:], 16), int(b[2:], 16))
    return int(spec[2:], 16)


# Emoji gabungan (ZWJ sequence) dan bendera subdivisi (tag sequence) sah dan
# dibuat oleh keyboard HP. Lindungi supaya tahap 1 tidak memecahnya.
_PICT = r"[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF]"
_MOD = r"[\uFE0F\U0001F3FB-\U0001F3FF]*"
EMOJI_SEQ_RE = re.compile(
    _PICT + _MOD + r"(?:\u200D" + _PICT + _MOD + r")+"
    r"|\U0001F3F4[\U000E0020-\U000E007E]+\U000E007F")


def protect_emoji(text):
    found = []

    def stash(m):
        found.append(m.group(0))
        return f"\x00EMO{len(found) - 1}\x00"

    return EMOJI_SEQ_RE.sub(stash, text), found


def restore_emoji(text, found):
    for i, seq in enumerate(found):
        text = text.replace(f"\x00EMO{i}\x00", seq)
    return text


# Kutipan pendek ("Halo guys, aku mau bahas") sering sengaja mencontohkan
# bahasa yang buruk. Jangan diganti dan jangan dihitung sebagai pola.
QUOTE_RE = re.compile(r'"[^"\n]{1,80}"')


def protect_quotes(text):
    found = []

    def stash(m):
        found.append(m.group(0))
        return f"\x00QUO{len(found) - 1}\x00"

    return QUOTE_RE.sub(stash, text), found


def restore_quotes(text, found):
    for i, q in enumerate(found):
        text = text.replace(f"\x00QUO{i}\x00", q)
    return text


def mask_quotes(text):
    return QUOTE_RE.sub('"kutipan"', text)


def protect_urls(text):
    """Swap URLs for placeholders so no pass rewrites inside a link."""
    found = []

    def stash(m):
        found.append(m.group(0))
        return f"\x00URL{len(found) - 1}\x00"

    return URL_RE.sub(stash, text), found


def restore_urls(text, found):
    for i, url in enumerate(found):
        text = text.replace(f"\x00URL{i}\x00", url)
    return text


def pass_invisible(text, lex):
    """Delete or space-normalise invisible characters. Returns (text, hits)."""
    hits = []
    for entry in lex["invisible"]:
        cp = _cp(entry["cp"])
        if isinstance(cp, tuple):
            pattern = "[" + re.escape(chr(cp[0])) + "-" + re.escape(chr(cp[1])) + "]"
        else:
            pattern = re.escape(chr(cp))
        n = len(re.findall(pattern, text))
        if n:
            hits.append({"name": entry["cp"] + " " + entry["name"], "count": n,
                         "action": entry["action"]})
            text = re.sub(pattern, "" if entry["action"] == "delete" else " ", text)
    # Any remaining Cf (format) character is invisible by definition.
    stray = [c for c in text if unicodedata.category(c) == "Cf"]
    if stray:
        hits.append({"name": "karakter format tak terlihat lainnya", "count": len(stray),
                     "action": "delete"})
        text = "".join(c for c in text if unicodedata.category(c) != "Cf")
    return text, hits


def pass_typographic(text, lex):
    hits = []
    for entry in lex["typographic"]:
        ch = entry["from"]
        n = text.count(ch)
        if not n:
            continue
        hits.append({"name": f"{ch} {entry['name']}", "count": n, "to": entry["to"].strip() or "(space)"})
        if ch == "—":
            # " word — word " and "word—word" both collapse to a comma + space.
            text = re.sub(r"\s*—\s*", ", ", text)
        elif ch == "–":
            text = re.sub(r"\s*–\s*(?=\d)", "-", text)      # 5–10  -> 5-10
            text = re.sub(r"\s+–\s+", ", ", text)            # used as em dash
            text = text.replace("–", "-")
        else:
            text = text.replace(ch, entry["to"])
    # A comma inserted before existing punctuation reads wrong.
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*\n", "\n", text)
    return text, hits


def _match_case(src, repl):
    if not repl:
        return repl
    if src.isupper() and len(src) > 1:
        return repl.upper()
    if src[0].isupper():
        return repl[0].upper() + repl[1:]
    return repl


def pass_lexical(text, lex):
    """Replace slop words and phrases. Longest first so phrases win."""
    hits = []
    entries = sorted(lex["phrases"] + lex["words"],
                     key=lambda e: len(e["find"]), reverse=True)
    for entry in entries:
        find = entry["find"]
        pattern = re.compile(r"\b" + re.escape(find).replace(r"\ ", r"\s+") + r"\b",
                             re.IGNORECASE)
        found = pattern.findall(text)
        if not found:
            continue
        hits.append({"find": find, "replace": entry["replace"] or "(dihapus)",
                     "count": len(found), "family": entry["family"]})
        text = pattern.sub(lambda m: _match_case(m.group(0), entry["replace"]), text)
    # Clean up after deletions. Deleting a whole clause leaves orphaned
    # punctuation behind ("system. ." or a line that now opens on a comma),
    # and that reads worse than the slop did.
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"(?m)^[ \t]*(?:[,.;:]+[ \t]*)+", "", text)
    text = re.sub(r"(?m)^[ \t](?=\S)", "", text)       # one space left by a deletion.
                                                      # Deeper indents are deliberate.
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)      # an em dash became a comma,
                                                      # then the clause after it went
    text = text.replace("...", "\x00ELL\x00")          # protect real ellipses
    text = re.sub(r"\.\s*\.+", ".", text)
    text = re.sub(r"([!?])\s*\.", r"\1", text)
    # Penutup yang dihapus meninggalkan tanda baca yatim: "membantu. ! dan tag".
    text = re.sub(r"(?<!\.)\.[ \t]*[!?]+", ".", text)
    text = text.replace("\x00ELL\x00", "...")
    text = re.sub(r"(?m)^[ \t]+$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # An em dash that became a comma, followed by a sentence connective, leaves
    # a splice ("is important, also, it's proof"). Promote it to a full stop.
    text = re.sub(r",\s*(also|so|still|basically|in the end|jadi|terus|intinya|makanya|ujungnya|belum lagi)\s*,\s*",
                  lambda m: ". " + m.group(1)[0].upper() + m.group(1)[1:] + ", ", text)
    return text, hits


def scan_structures(text, lex):
    flags = []
    for s in lex["structures"]:
        try:
            pattern = re.compile(s["regex"], re.MULTILINE)
        except re.error:
            continue
        found = pattern.findall(text)
        if found:
            flags.append({"name": s["name"], "count": len(found), "fix": s["fix"]})
    # Sentence-length uniformity is structural too.
    flat = re.sub(r"(?<=\d)[.,](?=\d)", "", text)      # Rp5.000 bukan akhir kalimat
    # Kalimat pendek ("Gratis.") justru tanda manusia, jadi ikut dihitung.
    lens = [len(s.split()) for s in SENT_RE.findall(flat) if len(s.split()) >= 1]
    if len(lens) >= 4:
        mean = sum(lens) / len(lens)
        var = sum((n - mean) ** 2 for n in lens) / len(lens)
        cv = (var ** 0.5) / mean if mean else 0
        if cv < 0.35:
            flags.append({
                "name": f"Panjang kalimat seragam (variasi {cv:.2f})",
                "count": len(lens),
                "fix": "Pecah satu kalimat jadi dua. Biarkan yang lain panjang. Mesin menulis rata.",
            })
    return flags


def restore_capitals(original, text):
    """Deleting an opener leaves the next word lower case.

    Only fix it for writers who capitalise their sentences in the first place:
    a deliberately lower-case voice is a style, not an artefact, and shouting
    over it would be exactly the kind of thing this script exists to stop.
    """
    starts = re.findall(r"(?:^|[.!?]\s+|\n)\s*([A-Za-z])", original)
    if not starts or sum(1 for c in starts if c.isupper()) * 2 < len(starts):
        return text
    return re.sub(r"(?:^|(?<=[^.]\. )|(?<=[!?] )|(?<=[.!?]\n)|(?<=\n))\s*([a-z])",
                  lambda m: m.group(0)[:-1] + m.group(1).upper(), text)


def humanize(text, lex):
    raw_for_case = text
    text, urls = protect_urls(text)
    text, emojis = protect_emoji(text)
    text, inv = pass_invisible(text, lex)
    text, typo = pass_typographic(text, lex)
    text, quotes = protect_quotes(text)
    text, lexi = pass_lexical(text, lex)
    # Satu penggantian bisa membentuk frasa klise baru ("sangat krusial" ->
    # "sangat penting"), jadi jalankan sekali lagi.
    text, lexi2 = pass_lexical(text, lex)
    lexi += lexi2
    text = restore_quotes(text, quotes)
    text = restore_capitals(raw_for_case, text)
    text = restore_emoji(text, emojis)
    text = restore_urls(text, urls)
    return text.strip() + "\n", {
        "invisible": inv,
        "typographic": typo,
        "lexical": lexi,
        "structures": scan_structures(mask_quotes(text), lex),
    }


def render_report(report, out=sys.stderr):
    def head(title):
        print(f"\n{title}\n" + "-" * len(title), file=out)

    total = sum(h["count"] for h in report["invisible"]) \
        + sum(h["count"] for h in report["typographic"]) \
        + sum(h["count"] for h in report["lexical"])

    head("LAPORAN HUMANIZE")
    print(f"{total} jejak mesin dihapus, "
          f"{len(report['structures'])} pola struktural ditandai untuk ditulis ulang", file=out)

    if report["invisible"]:
        head("1. KARAKTER TAK TERLIHAT")
        for h in report["invisible"]:
            act = {"delete": "hapus", "space": "spasi biasa"}.get(h["action"], h["action"])
            print(f"  {h['count']:>3}x  {h['name']}  -> {act}", file=out)
    if report["typographic"]:
        head("2. TIPOGRAFI")
        for h in report["typographic"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['to']}", file=out)
    if report["lexical"]:
        head("3. LEKSIKON BAHASA AI")
        for h in report["lexical"]:
            print(f"  {h['count']:>3}x  {h['find']}  -> {h['replace']}   [{h['family']}]", file=out)
    if report["structures"]:
        head("4. POLA STRUKTURAL  (tidak diperbaiki otomatis - tulis ulang sendiri)")
        for h in report["structures"]:
            print(f"  {h['count']:>3}x  {h['name']}\n        {h['fix']}", file=out)
    if not any(report.values()):
        head("BERSIH")
        print("  Tidak ada yang perlu dihapus.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Hapus sidik jari mesin dari draf.")
    ap.add_argument("input", nargs="?", default="-", help="file, or - for stdin")
    ap.add_argument("-o", "--out", help="write cleaned text here instead of stdout")
    ap.add_argument("--report", action="store_true", help="print what changed, to stderr")
    ap.add_argument("--json", action="store_true", help="emit {text, report} as JSON")
    ap.add_argument("--lexicon", default=LEX, help="path to slop.json")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    lex = load_lexicon(args.lexicon)
    clean, report = humanize(raw, lex)

    if args.json:
        print(json.dumps({"text": clean, "report": report}, indent=2, ensure_ascii=False))
        return
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(clean)
        print(f"ditulis ke {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(clean)
    if args.report:
        render_report(report)


if __name__ == "__main__":
    main()
