#!/usr/bin/env python3
"""
swipe.py - urutkan Reels yang kamu kumpulkan berdasarkan seberapa jauh mereka
mengalahkan akunnya sendiri, beri nama formula hook-nya, dan tulis swipe file.

Inti script ini satu koreksi: views mentah bukan bukti. Akun 2 juta follower
dapat 400 ribu views itu hari yang sepi. Akun 4 ribu follower dapat 400 ribu
views itu menemukan sesuatu. Script ini mengurutkan berdasarkan kelipatan
terhadap baseline akun itu sendiri ("outlier multiple").

Input berupa file dipisah TAB yang kamu isi sambil browsing, satu Reel per
baris, dengan baris judul kolom:

    account   followers   median   views    hook
    @akun     48rb        11rb     412rb    nggak ada yang bilang 30 reels pertama bakal sepi

Angka boleh ditulis seperti yang tampil di Instagram versi Indonesia: "412rb",
"1,2jt", "12,5K", "1.2M", "48.000". Versi aslinya membuang semua yang bukan
digit, jadi "1,2jt" terbaca 12. Di sini sudah dibaca benar (1.200.000).

`median` = views tipikal akun itu belakangan ini, baseline yang lebih baik.
Kalau cuma punya `followers`, kosongkan median dan script akan bilang.
`hook` = kalimat pertama Reel, diucapkan atau di layar, persis kata-kata mereka.

Pemakaian
  python3 swipe.py tangkapan.tsv
  python3 swipe.py tangkapan.tsv --out ~/.claude/instagram/swipe.md
  python3 swipe.py tangkapan.tsv --json
"""

import argparse
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HOOKS = os.path.join(HERE, "..", "ig-reel", "hooks.json")
WORD_RE = re.compile(r"[\w$%'’-]+")

try:                                              # optional: score the hooks too
    sys.path.insert(0, os.path.join(HERE, "..", "ig-reel"))
    from hookscore import run as score_hook       # noqa: E402
except Exception:                                 # ig-viral copied on its own
    score_hook = None


def parse_count(raw):
    """'412rb' -> 412000, '1,2jt' -> 1200000, '1.2M' -> 1200000, '48.000' -> 48000."""
    t = (raw or "").strip().lower().replace(" ", "")
    if not t:
        return None
    m = re.match(r"^([\d.,]+)(rb|ribu|k|jt|juta|m|mio|mil|miliar|b)?$", t)
    if not m:
        digits = re.sub(r"[^\d]", "", t)
        return int(digits) if digits else None
    num, unit = m.groups()
    mult = {"rb": 1e3, "ribu": 1e3, "k": 1e3, "jt": 1e6, "juta": 1e6, "m": 1e6,
            "mio": 1e6, "mil": 1e9, "miliar": 1e9, "b": 1e9}.get(unit, 1)
    if mult == 1:
        return int(re.sub(r"[.,]", "", num))                 # 48.000 / 48,000
    # Dengan satuan, satu-satunya pemisah adalah desimal: 1,2jt = 1.2M.
    num = num.replace(",", ".")
    if num.count(".") > 1:
        num = num.replace(".", "", num.count(".") - 1)
    try:
        return int(round(float(num) * mult))
    except ValueError:
        return None


def load_formulas(path):
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception:
        return None
    by_id = {h["id"]: h for h in d["hooks"]}
    order = d.get("classify_order") or sorted(by_id)
    return [(by_id[i]["id"], by_id[i]["name"],
             re.compile(by_id[i]["match"], re.IGNORECASE)) for i in order if i in by_id]


def classify(hook, formulas):
    if not formulas:
        return None, "belum terklasifikasi"
    for fid, name, pattern in formulas:
        if pattern.search(hook):
            return fid, name
    return None, "belum terklasifikasi"


def read_rows(path):
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    lines = [l for l in raw.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    if not lines:
        return []
    alias = {"akun": "account", "pengikut": "followers", "follower": "followers",
             "tayangan": "views", "view": "views", "putar": "views", "kalimat": "hook",
             "durasi": "length", "teks layar": "on-screen", "ajakan": "cta"}
    head = [alias.get(c.strip().lower(), c.strip().lower()) for c in lines[0].split("\t")]
    if "views" in head and "hook" in head:
        cols, body = head, lines[1:]
    else:
        cols, body = ["account", "followers", "views", "hook"], lines
    rows = []
    for line in body:
        cells = line.split("\t")
        if len(cells) < len(cols):
            cells += [""] * (len(cols) - len(cells))
        r = dict(zip(cols, [c.strip() for c in cells]))
        r["views"] = parse_count(r.get("views", "")) or 0
        for k in ("followers", "median"):
            r[k] = parse_count(r.get(k, "") or "")
        if r["views"] and r.get("hook"):
            rows.append(r)
    return rows


def analyse(rows, formulas):
    used_median = any(r.get("median") for r in rows)
    for r in rows:
        base = r.get("median") or r.get("followers") or 0
        r["baseline"] = base
        r["outlier"] = round(r["views"] / base, 2) if base else None
        r["formula_id"], r["formula"] = classify(r["hook"], formulas)
        r["words"] = len(WORD_RE.findall(r["hook"]))
        if score_hook:
            _, overall, verdict, _ = score_hook(r["hook"])
            r["hook_score"], r["hook_verdict"] = round(overall, 1), verdict
        else:
            r["hook_score"], r["hook_verdict"] = None, None
    ranked = sorted(rows, key=lambda r: -(r["outlier"] or 0))
    third = max(1, len(ranked) // 3)
    top, bottom = ranked[:third], ranked[-third:]

    def med(items, key):
        vals = [i[key] for i in items if i.get(key) is not None]
        return round(statistics.median(vals), 1) if vals else None

    counts = {}
    for r in top:
        counts[r["formula"]] = counts.get(r["formula"], 0) + 1
    return {
        "baseline": "median akun" if used_median else "jumlah follower",
        "n": len(ranked),
        "accounts": len({r.get("account", "") for r in ranked}),
        "reels": ranked,
        "top_formulas": sorted(counts.items(), key=lambda kv: -kv[1]),
        "top_hook_score": med(top, "hook_score"),
        "bottom_hook_score": med(bottom, "hook_score"),
        "top_words": med(top, "words"),
        "bottom_words": med(bottom, "words"),
        "unclassified": sum(1 for r in ranked if r["formula"] == "belum terklasifikasi"),
    }


def render(a, out=sys.stdout):
    head = (f"SWIPE FILE  ·  {a['n']} reels  ·  {a['accounts']} akun  ·  "
            f"baseline: {a['baseline']}")
    print("\n" + head, file=out)
    print("=" * max(len(head), 78), file=out)
    for r in a["reels"]:
        mult = f"{r['outlier']:.1f}x" if r["outlier"] else "   ?"
        score = f"{r['hook_score']:.0f}" if r["hook_score"] is not None else " -"
        fid = f"#{r['formula_id']:<2}" if r["formula_id"] else "-  "
        print(f"  {mult:>7}  hook {score:>3}  {fid} {r['formula'][:22]:<22} "
              f"{r.get('account', '')[:16]:<16} {r['views']:>11,}".replace(",", "."), file=out)
        print(f"           \"{r['hook'][:96]}\"", file=out)
    print("-" * max(len(head), 78), file=out)
    print("YANG JALAN DI BATCH INI", file=out)
    if a["top_formulas"]:
        print("  sepertiga teratas:     "
              + ", ".join(f"{n} x{c}" for n, c in a["top_formulas"][:4]), file=out)
    if a["top_hook_score"] is not None:
        print(f"  median skor hook:      atas {a['top_hook_score']:.0f}  "
              f"vs bawah {a['bottom_hook_score']:.0f}", file=out)
    print(f"  median panjang hook:   atas {a['top_words']} kata  "
          f"vs bawah {a['bottom_words']} kata", file=out)
    print(f"  belum terklasifikasi:  {a['unclassified']} dari {a['n']}. Baca manual, di situlah "
          "formula yang belum kamu punya bersembunyi.", file=out)
    print("\n  Batch yang dikumpulkan manual itu petunjuk, bukan bukti. Dua belas Reels tidak "
          "menunjukkan apa-apa;\n  empat puluh dari enam akun menunjukkan sesuatu. Kumpulkan "
          "lebih banyak sebelum percaya.\n", file=out)


def to_markdown(a):
    lines = ["# Swipe file", "",
             f"{a['n']} reels dari {a['accounts']} akun. "
             f"Diurutkan berdasarkan kelipatan terhadap {a['baseline']}.", ""]
    for r in a["reels"]:
        mult = f"{r['outlier']:.1f}x" if r["outlier"] else "?"
        lines += [f"## {mult}  {r['formula']}  ({r.get('account', '')})",
                  f"- views: {r['views']:,}  baseline: {r['baseline']:,}".replace(",", "."),
                  f"- skor hook: {r['hook_score']}  kata: {r['words']}",
                  f"- hook: \"{r['hook']}\"", ""]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Urutkan Reels berdasarkan outlier multiple.")
    ap.add_argument("input", nargs="?", default="-", help="file TSV, atau - untuk stdin")
    ap.add_argument("--hooks", default=HOOKS, help="path ke ig-reel/hooks.json")
    ap.add_argument("--out", help="tulis juga swipe file markdown ke sini")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = read_rows(args.input)
    if not rows:
        print("tidak ada baris yang bisa dipakai. Butuh file dipisah TAB, minimal kolom views dan hook.",
              file=sys.stderr)
        sys.exit(2)
    formulas = load_formulas(args.hooks)
    a = analyse(rows, formulas)
    if not formulas:
        print("catatan: hooks.json tidak ketemu, formula tidak dinamai. Pakai --hooks.", file=sys.stderr)
    if score_hook is None:
        print("catatan: hookscore.py tidak bisa diimpor, skor hook dilewati.", file=sys.stderr)

    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    if args.out:
        path = os.path.expanduser(args.out)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").write(to_markdown(a))
        print(f"ditulis ke {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
