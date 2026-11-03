#!/usr/bin/env python3
"""
idlang.py - alat bahasa Indonesia yang dipakai bersama oleh hookscore.py,
beats.py dan swipe.py.

Kenapa ada file ini: versi aslinya menghitung durasi dari jumlah KATA dengan
laju 165 kata per menit. Itu angka untuk bahasa Inggris. Kata bahasa
Indonesia rata-rata lebih panjang ("mempertanggungjawabkan" itu satu kata,
tujuh suku kata), jadi menghitung kata membuat naskah Indonesia selalu
terlihat lebih pendek dari aslinya.

Di sini durasi dihitung dari SUKU KATA. Ejaan bahasa Indonesia sangat teratur,
jadi jumlah suku kata hampir sama dengan jumlah kelompok vokal. Angka
dibacakan dulu ("Rp18.000" -> "delapan belas ribu rupiah") karena yang
dihitung adalah yang diucapkan, bukan yang ditulis.

Tidak ada dependensi, tidak ada jaringan.
"""

import re

# ---------------------------------------------------------------- angka

_SATUAN = ["", "satu", "dua", "tiga", "empat", "lima", "enam", "tujuh",
           "delapan", "sembilan", "sepuluh", "sebelas"]


def terbilang(n):
    """1250000 -> 'satu juta dua ratus lima puluh ribu'."""
    n = int(n)
    if n < 0:
        return "minus " + terbilang(-n)
    if n < 12:
        return _SATUAN[n] if n else "nol"
    if n < 20:
        return _SATUAN[n - 10] + " belas"
    if n < 100:
        sisa = n % 10
        return (_SATUAN[n // 10] + " puluh" + (" " + _SATUAN[sisa] if sisa else "")).strip()
    if n < 200:
        return ("seratus " + (terbilang(n - 100) if n > 100 else "")).strip()
    if n < 1000:
        sisa = n % 100
        return (_SATUAN[n // 100] + " ratus " + (terbilang(sisa) if sisa else "")).strip()
    if n < 2000:
        return ("seribu " + (terbilang(n - 1000) if n > 1000 else "")).strip()
    for nilai, nama in ((10 ** 12, "triliun"), (10 ** 9, "miliar"),
                        (10 ** 6, "juta"), (10 ** 3, "ribu")):
        if n >= nilai:
            depan, sisa = divmod(n, nilai)
            return (terbilang(depan) + " " + nama + " "
                    + (terbilang(sisa) if sisa else "")).strip()
    return str(n)


# Pemisah ribuan: Indonesia pakai titik (18.000), Inggris pakai koma (18,000).
# Koma desimal Indonesia (4,5 juta) hanya punya 1-2 digit di belakangnya, jadi
# tiga digit tepat di belakang pemisah dianggap ribuan.
_THOUSANDS_RE = re.compile(r"(?<![\d.,])\d{1,3}(?:[.,]\d{3})+(?![\d])")


def normalize_numbers(text):
    """'Rp18.000.000' -> 'Rp18000000'; '$18,000' -> '$18000'. Desimal tetap."""
    return _THOUSANDS_RE.sub(lambda m: re.sub(r"[.,]", "", m.group(0)), text)


# Satuan yang menempel atau mengikuti angka, dan bunyinya saat diucapkan.
UNIT_SPOKEN = {
    "rp": "rupiah", "%": "persen", "$": "dolar", "k": "ribu", "rb": "ribu",
    "ribu": "ribu", "jt": "juta", "juta": "juta", "m": "miliar", "miliar": "miliar",
    "kg": "kilo", "gr": "gram", "km": "kilometer", "m2": "meter persegi",
    "kw": "kilowat", "kwh": "kilowat jam", "w": "wat", "wp": "wat pik",
    "x": "kali", "jam": "jam", "menit": "menit", "mnt": "menit", "detik": "detik",
    "hari": "hari", "bulan": "bulan", "bln": "bulan", "tahun": "tahun", "thn": "tahun",
    "th": "tahun", "hrs": "hours", "min": "minutes",
}

NUMBER_TOKEN_RE = re.compile(r"^(rp|\$)?(\d+)(?:[.,](\d+))?([a-z%]*)$", re.IGNORECASE)


def spoken_form(token):
    """Bentuk ucapan satu token. 'Rp18000' -> 'delapan belas ribu rupiah'."""
    m = NUMBER_TOKEN_RE.match(token)
    if not m:
        return token
    prefix, whole, frac, unit = m.groups()
    parts = [terbilang(int(whole))]
    if frac:
        parts.append("koma " + " ".join(_SATUAN[int(d)] or "nol" for d in frac))
    unit = (unit or "").lower()
    if unit:
        parts.append(UNIT_SPOKEN.get(unit, " ".join(unit)))   # huruf dieja
    if prefix:
        parts.append(UNIT_SPOKEN[prefix.lower()])
    return " ".join(parts)


# ----------------------------------------------------------- suku kata

VOWELS = set("aeiouy")
DIPHTHONGS_FINAL = ("ai", "au", "oi", "ei")     # pantai, pulau, amboi, survei

# Singkatan chat yang tidak punya vokal tapi tetap diucapkan.
ABBREV_SYLLABLES = {
    "yg": 1, "dgn": 3, "dg": 3, "gw": 1, "gk": 1, "ga": 1, "tdk": 2, "krn": 2,
    "utk": 2, "sdh": 2, "jg": 2, "lg": 2, "bgt": 2, "tp": 2, "sm": 2, "dr": 2,
    "dlm": 2, "spt": 2, "kpd": 2, "pd": 1, "hrs": 2, "blm": 2, "bs": 2,
    "dm": 2, "ig": 2, "ui": 2, "ai": 2, "ok": 2, "cs": 2, "cta": 3, "fyp": 3,
}


# Singkatan yang dieja per huruf: U-EM-KA-EM, TE-HA-ER.
SPELLED = {"umkm", "bpjs", "asn", "pns", "thr", "ktp", "npwp", "ojk", "bri", "bca",
           "bni", "ump", "umr", "cpns", "seo", "roi", "ceo", "hrd", "kpr", "cod",
           "dp", "pdf", "hp", "wa", "ui", "ux", "ai", "plts", "pln", "ppn", "pph"}


def syllables_word(word):
    """Perkiraan suku kata satu kata (bahasa Indonesia, cukup untuk Inggris)."""
    raw = word.strip("'’\"-")
    w = raw.lower()
    if not w:
        return 0
    if w in SPELLED or (raw.isupper() and raw.isalpha()
                        and (len(raw) <= 3 or not set(w) & VOWELS)):
        return len(w)
    if w in ABBREV_SYLLABLES:
        return ABBREV_SYLLABLES[w]
    if any(ch.isdigit() for ch in w):
        spoken = spoken_form(w)
        if spoken != w:
            return sum(syllables_word(p) for p in spoken.split())
    # Kata ulang ("anak-anak", "berkali-kali") dihitung per bagian.
    if "-" in w:
        return sum(syllables_word(p) for p in w.split("-") if p)
    letters = re.sub(r"[^a-z]", "", w)
    if not letters:
        return 1
    count = 0
    run = ""
    for i, ch in enumerate(letters + " "):
        if ch in VOWELS and not (ch == "y" and run == "" and i + 1 < len(letters)
                                 and letters[i + 1] in VOWELS):
            run += ch
            continue
        if run:
            n = len(run)
            # Diftong di akhir kata dihitung satu: pan-tai, pu-lau.
            if i == len(letters) and n >= 2 and run[-2:] in DIPHTHONGS_FINAL:
                n -= 1
            # Pasangan vokal Inggris yang dibaca satu: "team", "book", "road".
            n -= len(re.findall(r"ee|oo|ea|oa|ou", run))
            count += max(1, n)
            run = ""
    if count == 0:
        return max(1, len(letters) // 2)            # singkatan tanpa vokal
    # "e" mati di akhir kata Inggris (make, save, love), bukan Indonesia (bare, kale).
    if letters.endswith(("ake", "ave", "ove", "ike", "ime", "ine", "ose", "ote", "ule")) and count > 1:
        count -= 1
    return count


WORD_RE = re.compile(r"(?:rp|\$)?[\w'’%-]+", re.IGNORECASE)


def words(text):
    """Kata yang diucapkan. 'Rp18.000' satu kata, 'anak-anak' satu kata."""
    return [w for w in WORD_RE.findall(normalize_numbers(text)) if w.strip("-_")]


def syllables(text):
    return sum(syllables_word(w) for w in words(text))


# ------------------------------------------------------------ kosakata

# Kata fungsi, untuk mendeteksi "loop" (kata dari hook yang diulang di akhir).
STOPWORDS = {
    # Indonesia
    "yang", "dan", "di", "ke", "dari", "ini", "itu", "aku", "saya", "gue", "gw",
    "kamu", "kalian", "lo", "lu", "kita", "kami", "dia", "mereka", "ada", "untuk",
    "buat", "dengan", "sama", "jadi", "tapi", "juga", "udah", "sudah", "belum",
    "nggak", "gak", "ga", "tidak", "bukan", "aja", "saja", "sih", "dong", "kok",
    "deh", "nih", "tuh", "kan", "ya", "yah", "lagi", "akan", "bisa", "mau",
    "harus", "kalau", "kalo", "karena", "soalnya", "biar", "atau", "pun", "lah",
    "kah", "si", "sang", "para", "pada", "dalam", "oleh", "seperti", "kayak",
    "banget", "sangat", "lebih", "paling", "satu", "se", "nya", "tiap", "semua",
    "pas", "waktu", "saat", "terus", "lalu", "habis", "abis", "cuma", "hanya",
    # Inggris
    "the", "a", "an", "and", "or", "but", "if", "of", "to", "in", "on", "for",
    "with", "that", "this", "it", "is", "are", "was", "were", "be", "been",
    "you", "your", "i", "my", "me", "we", "our", "they", "them", "he", "she",
    "so", "just", "not", "no", "do", "did", "does", "have", "has", "had",
    "will", "can", "at", "as", "by", "from", "out", "up", "off", "one", "all",
}

SPOKEN_NUMBERS = {
    # Indonesia. "satu" dan "pertama" sengaja tidak masuk: lebih sering pengisi
    # daripada jumlah.
    "dua", "tiga", "empat", "lima", "enam", "tujuh", "delapan", "sembilan",
    "sepuluh", "sebelas", "belas", "puluh", "puluhan", "ratus", "ratusan",
    "ribu", "ribuan", "juta", "jutaan", "miliar", "miliaran", "triliun",
    "seratus", "seribu", "sejuta", "setengah", "separuh", "seperempat",
    "lipat", "kali", "persen", "rb", "jt",
    # Inggris
    "zero", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "fifteen", "twenty", "thirty", "forty", "fifty",
    "hundred", "thousand", "million", "billion", "dozen", "half", "twice",
}

MONEY_WORDS = {
    "rupiah", "gaji", "gajian", "omzet", "omset", "cuan", "modal", "cicilan",
    "utang", "hutang", "harga", "ongkir", "profit", "duit", "uang", "untung",
    "thr", "bonus", "budget", "bujet", "biaya", "tagihan", "diskon", "promo",
    "dollars", "dollar", "bucks", "grand", "percent", "revenue", "salary", "rent",
}

# Kata yang mempertaruhkan sesuatu. Hook tanpa satu pun ini cuma pernyataan.
STAKES = {
    # Indonesia
    "stop", "berhenti", "jangan", "nggak", "gak", "ga", "enggak", "ngga", "tidak",
    "tak", "bukan", "belum", "salah", "kesalahan", "keliru", "rugi", "merugi",
    "kerugian", "boncos", "gagal", "kegagalan", "hilang", "kehilangan", "lenyap",
    "bangkrut", "dipecat", "resign", "ditolak", "diblokir", "dibanned", "kena",
    "ketipu", "ditipu", "penipuan", "scam", "bohong", "dibohongi", "jujur",
    "fakta", "rahasia", "ternyata", "padahal", "tapi", "malah", "justru", "cuma",
    "hanya", "tanpa", "sebelum", "sampai", "sampe", "nyesel", "menyesal",
    "bahaya", "berbahaya", "waspada", "awas", "gratis", "bayar", "dibayar",
    "mahal", "murah", "hemat", "boros", "habis", "abis", "dilarang", "ilegal",
    "terburuk", "benci", "buang", "dibuang", "sia-sia", "percuma", "masalah",
    "risiko", "harusnya", "seharusnya", "masih", "udah", "sudah", "vs", "versus",
    "pertama", "terakhir", "hapus", "dihapus", "ganti", "diganti", "mengganti",
    "menggantikan", "dibanding", "daripada", "kalah", "menang", "utang", "hutang",
    "telat", "terlambat", "mati", "rusak", "error", "tekor", "nombok", "dulu",
    "dulunya", "contek", "curi",
    # Inggris
    "never", "wrong", "mistake", "mistakes", "lost", "lose", "losing", "cost",
    "costs", "broke", "broken", "failed", "failure", "fail", "nobody", "no",
    "not", "don't", "dont", "doesn't", "didn't", "can't", "won't", "quit",
    "fired", "deleted", "delete", "killed", "replaced", "free", "paid", "saved",
    "first", "banned", "illegal", "worst", "hate", "wasted", "waste", "lie",
    "truth", "secret", "hidden", "before", "until", "instead", "but", "problem",
    "risk", "warning", "regret", "should", "still", "already", "only", "without",
    "actually",
}

# Kata ganti orang kedua. "kak", "bund", "moms" lazim dipakai menyapa penonton.
SECOND_PERSON = {
    "kamu", "kalian", "lo", "lu", "elo", "elu", "loe", "lw", "anda", "km", "kmu",
    "kak", "kakak", "bestie", "bes", "bun", "bunda", "moms", "sis", "gan", "bro",
    "you", "your", "you're", "youre", "yourself", "u",
}
FIRST_PERSON = {
    "aku", "saya", "gue", "gua", "gw", "ane", "kami", "kita", "i", "my", "me",
    "we", "our",
}
# Kata berakhiran -mu / -ku yang BUKAN kata ganti.
_NOT_MU = {"ilmu", "jamu", "tamu", "temu", "bertemu", "ketemu", "semu", "jemu",
           "kemu", "palu", "rumu", "menemu", "pramu", "mu"}
_NOT_KU = {"buku", "laku", "paku", "saku", "kuku", "suku", "miku", "selaku",
           "perilaku", "berlaku", "aku", "ku", "kaku", "baku", "taku", "haiku",
           "beku", "siku", "ragu", "ungu", "tengku", "bungku"}


def is_second_person(word):
    w = word.lower().strip("'’")
    return w in SECOND_PERSON or (len(w) > 3 and w.endswith("mu") and w not in _NOT_MU)


def is_first_person(word):
    w = word.lower().strip("'’")
    return w in FIRST_PERSON or (len(w) > 3 and w.endswith("ku") and w not in _NOT_KU)
