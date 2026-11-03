---
name: ig-reply
description: >-
  Menangani komentar di Reels dan post milik pengguna sendiri: memilah, lalu
  menulis balasan bahasa Indonesia untuk yang layak dibalas, termasuk "harga
  berapa kak", kritik, hater, calon pembeli, dan spam judi online. Gunakan saat
  pengguna menempelkan komentarnya, bilang "balasin komen ini", "handle komen
  di reels-ku", "ada yang komen X", atau sedang menghadapi kritik, hater, atau
  calon pembeli di kolom komen.
---

# ig-reply

Kolom komen di post sendiri adalah tempat jangkauan diputuskan. Setiap balasan
adalah interaksi tambahan di post itu, balasan di jam pertama melakukan
sebagian besar pekerjaan, dan di Instagram balasan juga bisa berupa Reel, yang
merupakan langkah paling jarang dipakai di platform ini.

Tapi nilai tiap komen tidak sama, jadi skill ini memilah sebelum menulis.

## Input

Pengguna menempelkan komennya, idealnya dengan handle. Screenshot boleh. Jangan
scraping thread-nya dengan alat browser.

## Pilah dulu

Masukkan setiap komen ke salah satu dari enam kelompok dan sebutkan jumlahnya:

| kelompok | apa itu | dapat apa |
| --- | --- | --- |
| **KATA KUNCI** | kata yang kamu minta dikomen ("MAU") | yang dijanjikan, dikirim manual atau lewat alat resmi |
| **CALON** | orang yang menceritakan masalah yang kamu selesaikan, atau "harga berapa kak?", "bisa kirim ke Makassar?" | jawaban nyata di publik, lalu pintu |
| **ISI** | menambah data, tidak setuju, mengembangkan | balasan terpanjang di thread |
| **PERTANYAAN** | pertanyaan yang dimiliki banyak orang | yang ini jadi Reel, bukan cuma balasan |
| **DUKUNGAN** | "🔥", "mantap kak", "izin save", tag teman | like, dan 3 sampai 8 kata paling banyak |
| **NOISE** | jualan, spam, niat buruk, pancingan, **promosi judi online ("slot gacor")** | tidak ada, atau satu kalimat lalu pergi; spam disembunyikan/dihapus |

Tulis dengan urutan itu dan berhenti saat nilainya habis.

## Langkah yang paling sering terlewat

Kalau satu pertanyaan di komen juga dimiliki tiga puluh orang lain, **balas
dengan Reel**. Instagram melampirkan komentarnya ke video baru sebagai stiker,
yang bertanya dapat notifikasi, dan pertanyaan dengan permintaan nyata jadi
post dengan hook yang sudah tertulis. Tandai setiap PERTANYAAN yang memenuhi
syarat dan serahkan ke `/ig-reel` sebagai formula #16.

## Cara membalas

- **Jawab pertanyaannya.** Kalau orang tanya caranya, beri tahu caranya, di
  balasan itu. Untuk "harga berapa kak?", **sebut harganya** kalau memang ada
  harga tetap. "Cek DM ya kak" untuk harga membuat banyak orang pergi dan
  terbaca seperti jebakan.
- **Sebut nama atau sapa sekali** di awal, tanpa tanda seru berlebihan. "Kak"
  wajar kalau memang itu budaya akunnya (ikuti `voice.md`).
- **Sesuaikan panjangnya.** Komen empat kata tidak dapat balasan empat baris.
- **Ke pengkritik:** akui bagian yang benar dulu, dengan kata-kata mereka, lalu
  pegang posisimu. Jangan menghapus, jangan defensif, jangan membalas dua kali
  di thread yang sama.
- **Ke hater:** tidak ada balasan. Balasan adalah jangkauan, dan itu yang mereka
  cari. Sembunyikan komennya kalau kasar. Kontrol komentar Instagram (Kata
  Tersembunyi, filter kata manual, batasi) ada untuk dipakai, dan memakainya
  bukan berarti kalah.
- **Ke calon pembeli:** jawab lengkap di publik. Pintunya satu kalimat di akhir,
  tawaran bantuan, bukan jualan. Jawaban publik itulah yang membuat orang
  berikutnya DM.

## Spam judi online

Komentar bot promosi judi online sangat umum di akun Indonesia. Jangan dibalas.
Sarankan pengguna menghapus atau menyembunyikannya, melaporkannya sebagai spam,
dan menambahkan kata-kata yang sering dipakai spam itu (misalnya "slot",
"gacor", "maxwin", "deposit") ke filter kata manual di pengaturan Komentar.
Spam yang dibiarkan membuat kolom komen terlihat tidak terurus.

## Komen kata kunci

Kalau post-nya memakai ajakan kata kunci, komen-komen itu adalah inti post-nya.
Setiap komen adalah orang yang mengangkat tangan. Balas masing-masing, lalu
kirim yang dijanjikan. Kalau pengguna sudah memakai otomatisasi lewat alat
Instagram sendiri atau partner resmi, bilang dan biarkan jalan; kalau belum,
balasannya manual dan itu tidak masalah di volume ini. Jangan pernah DM massal
ke orang yang tidak berkomentar.

## Output

Satu blok, dikelompokkan, tiap balasan siap-salin dan sudah lewat `/ig-human`:

```
BALASAN  ·  84 komen  ·  41 KATA KUNCI, 3 CALON, 3 ISI, 2 PERTANYAAN, 30 DUKUNGAN, 5 NOISE

KATA KUNCI  (41)  kirim file-nya. Satu baris tiap orang, hangat, jangan copy-paste persis.

CALON
@handle - "harga paket yang 50 toples berapa kak?"
> Rp1,2 juta kak, sudah termasuk label. Kalau mau, aku kirim contoh labelnya
> lewat DM.

PERTANYAAN -> REEL
@handle - "kalau cabainya lagi mahal gitu harganya ikut naik nggak?"
  34 like di komen ini. Ini Reel, bukan balasan. Formula #16.

NOISE  (5)  dilewati. 3 spam judi online: sembunyikan, laporkan, tambahkan ke filter.
```

(Harga contoh ilustrasi. Pakai harga pengguna, atau tanya.)

Lalu gerbangnya: tidak ada yang diposting sebelum pengguna bilang ya. Pengguna
yang menempelkan balasannya.
