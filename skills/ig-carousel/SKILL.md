---
name: ig-carousel
description: >-
  Membuat carousel Instagram berbahasa Indonesia: cover yang bikin orang
  menggeser, teks per slide, dan file 1080x1350 siap upload. Gunakan saat
  pengguna bilang "carousel", "slide", "postingan geser", "jadikan carousel",
  "bikin infografis IG", atau punya ide berbentuk daftar atau langkah yang
  akan mati kalau jadi satu gambar.
---

# ig-carousel

Carousel adalah format dengan waktu tonton terlama di grid, karena menggeser
adalah interaksi dan scroll bukan. Carousel juga dapat kesempatan kedua:
Instagram bisa menampilkannya lagi mulai dari slide berikutnya ke orang yang
tidak berinteraksi pertama kali, jadi slide dua juga harus bisa berdiri sendiri.

Format ini memberi hadiah untuk satu ide yang dipecah jadi langkah. Format ini
menghukum caption yang dipotong-potong.

## Kapan dipakai alih-alih Reel

Pakai carousel saat ide punya **urutan dan perlu dibaca ulang**: langkah,
kerangka dengan bagian-bagian, sebelum dan sesudah, daftar yang layak
di-screenshot (rincian modal, checklist, perbandingan harga). Pakai Reel saat
ide punya gerakan, wajah, atau hasil yang harus dilihat terjadi.

Kalau idenya satu klaim, bukan dua-duanya. Serahkan ke `/ig-reel` dan bilang.

## Struktur

6 sampai 10 slide. Batasnya 20 dan 20 hampir selalu jadi buku yang tidak
selesai dibaca. Di bawah 5, geseran tidak pernah dimulai.

```
1         COVER     hook-nya. Maksimal 6 kata, ukuran yang terbaca di grid
                    sebagai thumbnail. Satu baris janji di bawahnya.
2         TARUHAN   kenapa ini penting, satu kalimat. Slide ini juga cover
                    kedua, jadi tidak boleh cuma pengantar.
3 s.d. N  SATU IDE PER SLIDE. Judul 3 sampai 7 kata, maksimal 25 kata di
                    bawahnya. Kalau butuh satu paragraf, itu dua slide.
N+1       RANGKUMAN semuanya sebagai daftar. Ini slide yang di-screenshot.
TERAKHIR  CTA       satu aksi. Simpan, komen kata kunci, atau follow. Satu.
```

## Aturan teks slide

- **Cover adalah 80% hasilnya.** Enam kata. Besar. Tidak ada isi yang bisa
  menyelamatkan cover yang tidak digeser.
- **Kata bahasa Indonesia lebih panjang.** "Kesalahan" vs "mistake",
  "pengeluaran" vs "spend". Pilih kata yang pendek dan lazim ("salah", "biaya",
  "modal") supaya cover tetap enam kata dan tetap besar.
- **Desain untuk potongan grid.** Grid profil memotong jadi persegi panjang
  tegak, dan rasionya sudah beberapa kali berubah. Bangun di 1080x1350 dan
  taruh teks cover jauh di tengah, bebas dari 120 piksel terluar di semua sisi.
- **Beri nomor slide** (3/8). Orang lebih mungkin selesai kalau ujungnya kelihatan.
- **Tidak ada slide berupa paragraf.** Kalau tidak bisa dalam 25 kata, pecah.
- **Slide rangkuman yang di-screenshot dan dikirim.** Kiriman (share) adalah
  sinyal terkuat yang bisa didapat. Buat bisa berdiri sendiri tanpa konteks,
  termasuk dikirim ke grup WhatsApp.
- **Handle di setiap slide**, kecil, pojok bawah. Screenshot berjalan tanpa kamu.
- **Rupiah ditulis konsisten**: `Rp750 ribu` atau `Rp750.000`, pilih satu dalam
  satu carousel.
- **Alt text minimal di cover.** Dibaca pembaca layar dan oleh Instagram.

## Membuat filenya

Instagram mau 1080x1350 (4:5), JPEG atau PNG, maksimal 20 item. Buat sebagai
HTML lalu render tiap slide jadi gambar:

```bash
# satu <section> per slide, 1080x1350
# render dengan Playwright/Chromium (sudah terpasang di sesi cloud), satu PNG per slide
```

Tulis HTML dengan `width:1080px; height:1350px`, satu warna aksen, dan huruf
tidak lebih kecil dari 32px, karena dibaca di HP pada sepertiga ukuran aslinya.
Pastikan font mendukung karakter Indonesia dan emoji yang dipakai. Kalau
proyeknya punya brand skill atau design system, pakai itu dan jangan mengarang
palet.

Kirim PNG-nya ke pengguna. Lihat sendiri hasil render-nya sebelum mengirim:
teks terpotong, baris janda, atau cover yang tidak terbaca di ukuran thumbnail.

## Output

Teks per slide dulu, sebagai daftar bernomor yang bisa dibaca pengguna dalam
sepuluh detik dan diedit sebelum apa pun di-render. Lalu **caption**, yang untuk
carousel adalah Tugas B di `/ig-caption`: caption bekerja di sini, karena cover
sudah memakai enam katanya.

Jalankan keduanya lewat `/ig-human`. Buat file hanya setelah pengguna
menyetujui teksnya.

```
CAROUSEL  ·  8 slide

1  COVER      MODAL SAMBAL: RP750 RIBU
              Rinciannya sampai ke toples.
2  TARUHAN    Banyak yang nunda jualan karena ngira modalnya jutaan.
3             CABAI DAN BAWANG
              Rp310 ribu untuk 40 botol pertama.
...
7  RANGKUMAN  Semua pos biaya, satu tabel.
8  CTA        Komen MODAL dan aku kirim file hitungannya.

Caption: Tugas B, hook di baris 1, satu ajakan, 3 tag.
```

(Angka contoh ilustrasi. Pakai angka pengguna, atau `{{angkamu}}`.)

Tidak ada yang diunggah. Pengguna yang memposting.
