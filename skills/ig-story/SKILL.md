---
name: ig-story
description: >-
  Menulis Instagram Story harian berbahasa Indonesia: urutan per frame, stiker
  yang dipakai di mana, dan satu frame yang memindahkan orang ke DM. Gunakan
  saat pengguna bilang "story", "mau posting apa di story", "urutan story",
  "ide polling", "bingung mau story apa", "jualan lewat story", atau ingin
  menjual sesuatu tanpa membuat post soal itu.
---

# ig-story

Story bukan feed versi kecil. Feed adalah cara orang asing menemukanmu. Story
adalah cara orang yang sudah follow memutuskan apakah kamu orang yang layak
dibeli, dan satu-satunya tempat di Instagram di mana satu ketukan langsung jadi
percakapan.

Hampir tidak ada orang di luar follower yang melihat ini, jadi tugasnya beda
total: kedalaman, bukan jangkauan.

## Bentuk harian

Tiga sampai tujuh frame sehari. Lewat dari sekitar tujuh, tingkat ketuk-lewati
naik dan frame terakhir diputar untuk tidak ada siapa-siapa, padahal di situlah
orang biasanya menaruh ajakan.

```
1       PEMBUKA    sesuatu yang terjadi hari ini, ada wajah atau tangan di dalamnya.
2-3     TENGAH     isinya: prosesnya, hasilnya, kesalahannya.
4       AJAKAN     satu stiker. Polling, kotak pertanyaan, kuis, atau link.
5       PENUTUP    jawabannya, hasilnya, atau pancingan untuk besok.
```

Taruh ajakan di frame 4, bukan frame 7.

## Stiker, dan apa gunanya sebenarnya

| stiker | tugas | pakai saat |
| --- | --- | --- |
| **Polling** | ketukan termurah yang ada | butuh volume respons, bukan informasi |
| **Kotak pertanyaan** | memanen kata-kata persis yang dipakai audiens | butuh ide konten atau keberatan, apa adanya |
| **Kuis** | mengajar dengan membiarkan mereka salah | ada salah kaprah umum di niche-nya |
| **Slider emoji** | cek suasana | tidak ada yang penting. Seru, nilainya rendah |
| **Link** | satu-satunya permukaan yang bisa diklik selain bio | ada tujuan nyata (katalog, WA, form) |
| **Hitung mundur** | tenggat yang bisa diikuti | launching, live, PO ditutup, flash sale gajian |
| **Tambahkan punyamu (Add Yours)** | jangkauan di luar follower, sesekali | promptnya bisa dijawab siapa pun di niche itu |

Kotak pertanyaan adalah yang paling diremehkan. Setiap jawaban adalah caption,
hook Reel, atau pembuka DM yang ditulis dengan bahasa audiens sendiri. Serahkan
ke `/ig-reel` sebagai formula #16.

## Konteks Indonesia

- **Close Friends** cocok untuk pelanggan setia atau grup reseller: info stok,
  harga khusus, PO duluan. Jangan dipakai untuk menyembunyikan promosi dari
  follower lain lalu berpura-pura eksklusif.
- **Ritme kalender lokal** menggerakkan story: gajian (akhir dan awal bulan),
  Ramadan (sahur, ngabuburit, THR), mudik, Harbolnas 11.11 dan 12.12. Story
  hitung mundur paling masuk akal di momen-momen itu.
- **Link ke WhatsApp** wajar untuk bisnis di Indonesia. Satu link, satu tujuan.

## Aturan

- **Wajah atau tangan di frame pertama.** Teks di latar warna polos diketuk
  lewat, dan frame pertama menentukan sisanya ditonton atau tidak.
- **Satu ide per frame.** Tidak ada yang membaca paragraf di story.
- **Teks di tengah.** Di 1080x1920, jangan ada apa pun di atas y=250 atau di
  bawah y=1600. Baris profil di atas dan kolom balas di bawah.
- **Bicara ke satu orang.** "Kamu", bukan "kalian semua". Story adalah hal
  paling mirip DM yang bukan DM.
- **Jangan repost post feed sendiri ke story tanpa komentar.** Itu frame yang
  paling sering dilewati. Kalau menunjuk ke post, bilang apa yang terjadi di
  komennya dan kenapa layak dilihat.
- **Jualan di story, bukan di post.** Tiga frame konteks, satu frame tawaran,
  satu frame bukti (testimoni asli dengan izin, screenshot pesanan dengan data
  pembeli disensor). Urutan itu menjual lebih banyak daripada post feed soal
  hal yang sama dan tidak memakan jangkauan.

## Funnel DM, dengan jujur

Urutan yang jalan: story yang menyebut masalah, kotak pertanyaan atau polling
yang memberi orang kesempatan bilang "itu aku banget", lalu balasan ke setiap
orang yang menjawab. Percakapan dimulai karena mereka yang bicara duluan.

Balasan DM otomatis berbasis kata kunci adalah fitur resmi untuk akun
profesional, lewat alat Instagram sendiri atau partner yang disetujui. Kirim DM
massal ke orang yang tidak berinteraksi tidak, dan itu yang membuat akun
dibatasi. Aturannya sederhana: **mereka bergerak dulu, baru kamu membalas.**

## Output

Frame berurutan, masing-masing dengan isi layar, yang diucapkan, dan stikernya,
plus apa yang dilakukan dengan jawabannya:

```
STORY  ·  Selasa  ·  5 frame

1  [selfie, sambil jalan ke pasar]  "Cabai naik lagi. Ketiga kalinya bulan ini."
2  [rekaman layar]                  catatan harga cabai 4 minggu terakhir
3  [ngomong ke kamera]              "Harga sambal tetap. Yang aku ubah ukuran toplesnya."
4  [polling]                        "Kamu lebih pilih harga naik atau isi dikurangi?"  Harga / Isi
5  [teks di atas foto]              "Besok aku spill hitungannya."

Setelahnya: semua yang vote dapat balasan DM. Itu seluruh funnel-nya.
```

Gunakan register dan sapaan dari `voice.md`. Jalankan teksnya lewat `/ig-human`.
Tidak ada yang diposting. Pengguna yang memposting.
