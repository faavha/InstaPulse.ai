---
name: ig-repurpose
description: >-
  Mengubah satu aset panjang berbahasa Indonesia (video YouTube, podcast, live
  IG/TikTok, webinar, kajian, newsletter, artikel blog, rekaman rapat dengan
  klien) jadi seminggu Reels dan carousel yang masing-masing berdiri sendiri.
  Gunakan saat pengguna bilang "repurpose ini", "potong jadi reels", "aku punya
  video/podcast/transkrip", "jadikan konten IG", atau menempelkan sesuatu yang
  panjang dan ingin masuk Instagram.
---

# ig-repurpose

Satu aset panjang yang bagus berisi empat sampai enam post. Kebanyakan orang
mengambil satu dan membuang sisanya.

## Input

Transkrip, artikel, newsletter, naskah, ringkasan rapat, rekaman live. Kalau
pengguna memberi URL dan sesi ini punya alat transkrip, pakai; kalau tidak,
minta ditempel. Baca semuanya sebelum mengambil apa pun.

Transkrip otomatis bahasa Indonesia sering salah di nama, angka, istilah
Inggris, dan bahasa daerah. Tandai bagian yang meragukan dan konfirmasi ke
pengguna sebelum mengutipnya, apalagi angka.

Kalau sumbernya video milik pengguna, minta juga filenya. Reel yang dibangun
dari footage aslinya mengalahkan Reel yang cuma membacakan ulang kata-katanya.

## Ambil, jangan ringkas

Ringkasan video bukan Reel. Tidak ada yang mau ringkasannya. Telusuri asetnya
dan tarik hal-hal yang bisa berdiri sendiri:

| tarik | apa itu |
| --- | --- |
| **Klaim** | setiap kalimat yang bisa memulai perdebatan |
| **Angka** | setiap angka, biaya (Rp), durasi, persentase |
| **Cerita** | setiap momen dengan orang, adegan, dan harga yang dibayar |
| **Mekanisme** | setiap "cara kerjanya sebenarnya begini..." |
| **Kesalahan** | setiap pengakuan soal sesuatu yang gagal |
| **Kalimat** | setiap kalimat yang sudah layak dikutip apa adanya |

Daftar temuannya, dengan jumlahnya, sebelum menulis apa pun. Kalau asetnya
menghasilkan kurang dari empat, asetnya tipis, dan empat post yang diperas
darinya juga akan tipis. Katakan.

## Lalu pilih format per temuan

Tidak semuanya Reel.

- **Klaim, kesalahan, cerita** jadi Reel. Butuh suara dan wajah.
- **Mekanisme, daftar bernomor, rincian biaya** jadi carousel. Perlu dibaca ulang.
- **Kalimat yang layak kutip** jadi frame story, bukan post.

## Lalu susun minggunya

Setiap temuan jadi satu post dan setiap post berdiri sendiri sepenuhnya.
Penonton belum melihat sumbernya dan tidak akan pernah. Jangan pernah menulis
"seperti yang aku bilang di video terbaruku" atau "full-nya di YouTube ya".
Post-nya adalah barangnya.

Beri formula hook dari `ig-reel/hooks.json` ke masing-masing dan variasikan.
Lima post dari satu sumber dengan bentuk hook yang sama terbaca seperti pabrik
konten, karena memang begitu.

Kalau sumbernya video milik pengguna, **pakai footage aslinya**. Klip saat dia
mengatakannya, dengan reaksi aslinya, selalu mengalahkan rekaman ulang. Potong
di kalimat, bukan di tarikan napas.

Urutkan sepanjang minggu supaya klaim terkuat keluar pertama, cerita di tengah
minggu, dan mekanisme terakhir, saat orang yang menyukai yang sebelumnya sedang
menunggu.

## Output

```
SUMBER: "Kenapa kami berhenti kasih diskon ke teman" (podcast 42 menit, 7.100 kata)

DITEMUKAN  5 klaim, 9 angka, 3 cerita, 4 mekanisme, 2 kesalahan, 7 kalimat layak kutip

MINGGU
SEL  REEL      #2  Perintah Larangan  Stop kasih diskon ke teman
                                      pakai klip menit 14:20, dia ketawa di akhir
RAB  CAROUSEL  caption Tugas B        Template chat buat nolak minta diskon dengan sopan
JUM  REEL      #21 Mulai di Tengah    "...dan temanku itu yang paling telat bayarnya."
MIN  REEL      #5  Waktu Ringkas      Enam jam seminggu balik, karena satu kalimat di bio

Bilang "tulis Selasa" dan aku buatkan drafnya.
```

Lalu buat draf berdasarkan permintaan, satu per satu, masing-masing lewat
`/ig-reel` dan `/ig-human`. Jangan menumpahkan empat naskah jadi sekaligus.
Semuanya akan terdengar sama dan pengguna tidak akan merekam satu pun.
