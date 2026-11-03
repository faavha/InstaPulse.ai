---
name: ig-human
description: >-
  Menghapus jejak AI dari draf bahasa Indonesia (atau campuran Inggris): em dash,
  "bahasa AI" seperti "di era digital seperti sekarang ini", "bukan sekadar X
  tapi Y", "Anda/merupakan/tersebut" di akun santai, karakter tak terlihat,
  lalu menilainya dengan lima pemeriksaan. Gunakan saat pengguna bilang
  "humanize", "biar nggak kayak AI", "kok kayak ChatGPT", "hapus em dash",
  "bikin lebih natural", atau sebelum caption, naskah, komen, balasan atau DM
  ditunjukkan ke pengguna.
---

# ig-human

Dua script tinggal di folder skill ini dan keduanya jalan. Pakai. Jangan
menilai dengan mata.

```bash
python3 humanize.py draf.txt -o bersih.txt --report   # bersihkan, tunjukkan perubahan
python3 detect.py draf.txt                             # nilai, lima pemeriksaan
python3 detect.py draf.txt bersih.txt                  # buktikan selisihnya
python3 detect.py draf.txt --register formal           # untuk akun institusi
```

Keduanya membaca `slop.json`: kamus "bahasa AI" Indonesia (frasa terjemahan
kaku, pembuka basa-basi, penghubung formal, penutup refleks caption) ditambah
kamus asli bahasa Inggris untuk caption campuran, karakter tak terlihat, aturan
tipografi, dan pola struktural. File itu milik pengguna. Kalau ada kata yang
memang gaya mereka ("semoga bermanfaat" sebagai ciri khas, misalnya), hapus
entrinya.

## Kenapa ini lebih penting di Instagram

Caption pendek dan naskah diucapkan. Satu kalimat yang terasa tulisan di caption
600 karakter adalah porsi yang lebih besar daripada kalimat yang sama di
artikel. Di Indonesia tandanya punya warna sendiri: bahasa terjemahan ("Anda",
"merupakan", "sebuah", "memiliki"), pembuka gaya artikel SEO ("Di era digital
seperti sekarang ini..."), dan penutup gaya admin ("Semoga bermanfaat! Jangan
lupa like, follow dan share"). Orang yang scroll langsung mengenalinya sebagai
brand atau template, bukan manusia.

## Yang diperbaiki otomatis

**1. Karakter tak terlihat.** Zero-width space, word joiner, soft hyphen, BOM,
karakter tag Unicode, spasi tak-putus. Keyboard HP tidak menghasilkan ini.
**Pengecualian:** joiner di dalam emoji gabungan (👨‍💻, 👩‍👧‍👦, 🏳️‍🌈) dan bendera
tetap utuh. Versi aslinya memecah 👨‍💻 jadi 👨💻; di sini sudah diperbaiki.

**2. Tipografi.** Em dash jadi koma, en dash jadi tanda hubung, kutip
melengkung jadi lurus, elipsis jadi tiga titik, bullet jadi tanda hubung.

**3. Leksikon.** Contoh: "krusial" -> "penting", "secara signifikan" -> "jauh",
"oleh karena itu" -> "makanya", "di era digital seperti sekarang ini" ->
"sekarang", "mari kita bahas" dihapus, "semoga bermanfaat" dihapus, "jangan
lupa follow" dihapus. Penggantinya ditulis untuk register santai. Huruf
besar-kecil dipertahankan, URL tidak disentuh, dijalankan dua kali karena satu
penggantian bisa membentuk frasa klise baru.

## Yang TIDAK diperbaiki otomatis

Pola struktural **ditandai, bukan ditulis ulang**, karena mengubah bentuk
kalimat butuh penilaian:

- "Bukan sekadar X, tapi Y" dan "Tidak hanya X, tetapi juga Y"
- "Ini bukan tentang X. Ini tentang Y."
- Baris tanya satu kata: "Hasilnya?" "Faktanya?"
- "Berikut adalah 5 cara...:" dan "Yuk, simak!"
- "Pernahkah kamu merasa...?" dan "Bayangkan..."
- Pola tiga: "cepat, mudah, dan murah."
- Sapaan pembuka: "Halo sobat UMKM!"
- "Jangan lupa like, follow, share" dan "Tag teman kamu yang..."
- Bullet emoji (✅ ➡️ ✨), tembok hashtag, tiga kata kapital berturut-turut

Itu tugasmu. Tulis ulang tiap baris yang ditandai, pertahankan maknanya, lalu
jalankan `detect.py` lagi. Ini bagian yang memindahkan skor dari TINJAU ke
LULUS, dan bagian yang tidak bisa dilakukan script.

**Register kaku tidak diganti otomatis** ("Anda" -> "kamu" bisa salah kalau
akunnya memang formal). `detect.py` menghukumnya di pemeriksaan SUARA kalau
registernya santai. Ganti sendiri sesuai `voice.md`.

## Lima pemeriksaan

`detect.py` memberi skor 0-100 untuk lima sinyal, makin tinggi makin manusia:

| pemeriksaan | yang diukur | kalau mesin |
| --- | --- | --- |
| VARIASI | variasi panjang kalimat | semua kalimat sama panjang |
| KONKRET | angka, Rp, nama per 100 kata | kata benda abstrak, tanpa angka |
| KLISE | kata dari leksikon per 100 kata | kosakata template |
| SIDIK JARI | karakter tak terlihat, em dash, kutip melengkung | tipografi terlalu sempurna |
| SUARA | penanda lisan (nggak, udah, sih, banget), kata ganti, penanda kaku (Anda, merupakan, tersebut), pola struktural | tidak ada bahasa lisan, banyak bahasa terjemahan |

Vonis memberi bobot 60% ke rata-rata dan 40% ke **pemeriksaan terlemah**,
karena satu sinyal sudah cukup. LULUS butuh total 70+ dan tidak ada yang di
bawah 55.

Dengan `--register formal`, penanda lisan dan penanda kaku tidak dihitung.
Pakai untuk akun kampus, instansi, atau brand yang memang memakai "Anda".

## Katakan ini dengan jujur

Ini lima heuristik lokal yang meniru sinyal yang dipakai detektor publik.
Berjalan di komputer pengguna, tidak ada yang diunggah. Ini **bukan** GPTZero,
Originality, Copyleaks, Winston atau Turnitin, tidak memanggil API mereka, dan
tidak bisa menjanjikan vonis mereka. Ambang batasnya berasal dari versi asli
bahasa Inggris dan belum dikalibrasi pada korpus Indonesia. Jangan membuat
klaim yang lebih besar atas nama pengguna, dan jangan pernah bilang teksnya
"tidak terdeteksi".

## Urutan kerja

1. `humanize.py draf.txt -o bersih.txt --report`
2. Baca pola struktural yang ditandai. Tulis ulang baris-baris itu sendiri,
   termasuk mengganti register kaku kalau akunnya santai.
3. `detect.py draf.txt bersih.txt` untuk menunjukkan sebelum dan sesudah.
4. Kalau belum LULUS, perbaiki pemeriksaan terlemah yang disebut lalu ulangi.
   Dua putaran itu normal. Lima putaran berarti drafnya ditulis pakai rumus,
   dan solusinya draf baru, bukan putaran tambahan.
5. Tunjukkan teks bersih dan skornya ke pengguna. Jangan skornya saja.
