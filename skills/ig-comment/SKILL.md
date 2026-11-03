---
name: ig-comment
description: >-
  Menulis komentar bahasa Indonesia di post dan Reels orang lain yang terbaca
  seperti manusia yang punya pendapat, bukan bot atau akun "izin nyimak".
  Gunakan saat pengguna menempelkan post atau Reel dan minta komen, bilang
  "komenin ini", "engage ke post ini", "enaknya komen apa", atau butuh satu
  batch untuk putaran engagement harian.
---

# ig-comment

Berkomentar adalah dua puluh menit dengan daya ungkit tertinggi di Instagram,
dan paling gampang dilakukan dengan buruk. Komen di posisi atas Reel dengan 40
ribu views dilihat lebih banyak orang daripada post kebanyakan akun, dan itu
satu-satunya tempat orang asing bisa mengetuk langsung ke profil.

Komen generik lebih buruk daripada tidak ada. Ia membuang satu ketukan yang
tidak ke mana-mana dan menandai akun sebagai akun pod engagement di mata satu
orang yang pendapatnya penting: kreatornya.

## Input

Pengguna menempelkan teks post atau Reel, atau screenshot, dengan nama akunnya.
Kalau dikasih URL yang tidak bisa dibuka, minta ditempel. Jangan pakai alat
browser untuk scraping feed dan jangan memposting apa pun.

## Sembilan jenis komen

Pilih berdasarkan isi post-nya. Jangan default ke jenis 1.

| # | jenis | kapan | bentuk |
| --- | --- | --- | --- |
| 1 | **Tambah data** | post membuat klaim yang bisa didukung angka | "Sama di kami: 40% dari..." |
| 2 | **Tambah kasus yang hilang** | post-nya benar tapi belum lengkap | "Ini berlaku sampai {kondisi}." |
| 3 | **Beda pendapat dengan hormat** | kamu benar-benar menganggapnya keliru | sebut yang disetujui dulu, lalu bedanya |
| 4 | **Kembangkan satu kalimat** | ada satu kalimat yang paling bagus | kutip, lalu bangun di atasnya |
| 5 | **Tanya yang sebenarnya** | post-nya melewatkan bagian yang sulit | satu pertanyaan, spesifik |
| 6 | **Pengalaman** | kamu pernah melakukan yang dia ceritakan | apa yang terjadi, dua kalimat |
| 7 | **Koreksi** | ada kesalahan fakta | benar, singkat, sopan, yakin |
| 8 | **Sudut lain** | faktanya benar, bingkainya salah | "Cara lain membacanya:" |
| 9 | **Satu kalimat** | post-nya tidak butuh apa-apa, kamu ingin hadir | di bawah 10 kata, harus lucu atau benar |

## Aturan

- **Satu sampai tiga kalimat.** Komen dibaca di kolom sempit di bawah video.
  Paragraf dilipat di balik "selengkapnya" dan tidak ada yang mengetuknya.
- **Jangan pernah dibuka dengan** "Mantap kak", "Keren bang", "Nice info",
  "Izin save", "Izin nyimak", "Auto save", "Semangat terus kak", "Daging semua",
  "Bermanfaat banget", "Sangat menginspirasi", "Great post", atau nama kreator
  dengan tanda seru. Semuanya tidak terlihat.
- **Tidak ada komen emoji saja** ("🔥🔥🔥", "🙏") dan tidak ada emoji sebagai
  karakter pertama.
- **Jangan mengulang isi Reel-nya.** Semua yang nonton baru saja menontonnya.
- **Satu ide.** Komen dengan dua poin terbaca seperti membajak.
- **Katakan hal spesifik.** Kalau komennya bisa ditempel di post mana pun soal
  topik itu, itu bukan komen, itu noise.
- **Sapaan sesuai budaya akun itu.** "Kak" wajar di akun jualan dan banyak niche
  Indonesia; ikuti cara follower lain menyapa kreatornya, jangan sok akrab.
- **Tidak ada jualan, sama sekali.** Bukan tawaran, bukan link, bukan "mampir
  ke IG-ku ya kak", bukan "cek bio". Itu cara tercepat diblokir oleh orang yang
  justru ingin dijangkau.
- **Lebih awal lebih penting di sini.** Komen di jam pertama pada Reel yang
  kemudian menyebar ikut terbawa.

## Output

Beri **dua opsi dengan jenis berbeda**, diberi label, plus satu kalimat soal
mana yang akan kamu posting dan kenapa. Jalankan keduanya lewat `/ig-human`
dulu: komen pendek, jadi satu em dash atau satu frasa klise terdengar lebih
nyaring daripada di caption.

```
OPSI KOMEN  (di Reel @akun soal naikin harga)

[6 · Pengalaman]
Kami naikin harga 40% bulan Maret dan cuma kehilangan satu klien, yang
kebetulan paling banyak minta revisi. Butuh delapan bulan buat berhenti takut.

[3 · Beda pendapat]
Setuju soal anchoring-nya. Yang aku kurang setuju naikinnya di tengah proyek.
Kami pernah coba, dan itu bikin satu perpanjangan kontrak batal.

Posting yang pertama. Ada yang dia akui, dan ada angkanya.
```

(Angka contoh ilustrasi. Komen pengguna hanya boleh memakai angka pengguna.)

## Mode batch

Untuk putaran engagement, minta 5 sampai 10 post sebagai teks dalam satu pesan,
kembalikan satu komen untuk masing-masing dalam satu blok, dan catat di
`~/.claude/instagram/log.md` siapa saja yang sudah dikomentari minggu ini.
Berkomentar di tiga akun yang sama setiap hari itu kelihatan, dan kelihatan
persis seperti apa adanya.

## Jangan pernah

Jangan auto-post, jangan otomatisasi komen, jangan pakai alat browser untuk
memposting atas nama pengguna. Engagement otomatis melanggar Ketentuan
Penggunaan Instagram dan membuat akun dibatasi. Skill ini menulis komennya.
Pengguna yang memposting.
