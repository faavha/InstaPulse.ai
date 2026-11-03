---
name: ig-caption
description: >-
  Menulis caption Instagram berbahasa Indonesia: baris yang selamat dari
  potongan "... selengkapnya", isi, satu ajakan, kata pencarian, dan maksimal
  lima hashtag, lalu memeriksanya dengan linter. Gunakan saat pengguna bilang
  "bikinin caption", "caption buat post ini", "nulis deskripsi", "hashtag apa
  yang bagus", punya Reel atau carousel yang siap dan butuh teksnya, atau
  bertanya soal hashtag.
---

# ig-caption

Satu script tinggal di folder skill ini dan jalan:

```bash
python3 caption.py caption.txt
python3 caption.py caption.txt --keywords "jasa desain logo,logo umkm"
```

Script mencetak caption seperti feed mencetaknya: 125 karakter pertama di dalam
kotak, sisanya di balik ketukan. Baca kotak itu sebelum membaca apa pun yang
kamu tulis.

## Pertama, putuskan tugas caption ini

Ini keputusan yang merusak caption kalau dilewati.

**Tugas A: videonya sudah menangkap penonton.** Reel membawa hook-nya sendiri
di dua detik pertama, diucapkan dan di layar. Caption bukan hook kedua, dan
bersaing dengan video membuat dua-duanya kalah. Tugasnya: ajakan, konteks yang
membuat ajakan masuk akal, dan kata-kata yang dicari orang.

**Tugas B: caption adalah kontennya.** Foto, satu gambar, atau cover carousel
yang membuka rasa penasaran. Di sini baris pertama adalah hook dan bekerja
persis seperti hook Reel: konkret, pendek, dan terpotong di titik yang bikin
penasaran, bukan di tengah anak kalimat.

Tanyakan yang mana. Kalau pengguna punya Reel dengan hook kuat, tulis A dan
jelaskan kenapa.

## Bentuknya

```
Baris 1     125 karakter yang terlihat. Tugas A: ajakannya, terang-terangan.
            Tugas B: hook-nya.
            Bukan sapaan ("Halo sobat cuan!"), bukan salam, bukan hashtag,
            bukan emoji sebagai karakter pertama.
Isi         paragraf pendek, satu baris kosong di antaranya. Dua sampai enam.
            Di sinilah kata pencarian tinggal.
Ajakan      satu. Komen kata kunci, simpan, atau DM. Satu.
Hashtag     maksimal lima, di baris sendiri paling bawah, atau tidak ada.
```

Batasnya 2.200 karakter dan hampir tidak ada yang butuh 2.200. Caption yang
membuat orang mengetuk lalu memberi 600 karakter mengalahkan yang memberi 1.800.

## Hashtag, apa adanya

Hashtag bukan lagi tuas jangkauan, dan platformnya sudah mengatakan itu lewat
perubahan produk. **Sejak 18 Desember 2025 Instagram membatasi hashtag
maksimal lima per post atau Reel**, turun dari tiga puluh, dengan alasan
beberapa tag yang tertarget lebih baik daripada banyak tag generik. Batas lima
itu dihitung gabungan caption dan komentar.

Jadi: maksimal lima, spesifik, sebagai label topik. Kalau pengguna punya blok
30 hashtag tersimpan di Notes HP, blok itu sekarang beban mati dan linter akan
menggagalkannya.

`#fyp`, `#fypシ`, `#viral`, `#viralindonesia`, `#explore`, `#reelsinstagram`,
`#masukberanda` tidak mendeskripsikan apa-apa. Buang.

## Kata pencarian lebih penting daripada hashtag

Pencarian Instagram membaca teks caption. Jadi frasa yang ingin dicarikan
masuk ke caption sebagai frasa yang diketik manusia, dalam kalimat yang
terbaca wajar. "Jasa desain logo" sebagai kata-kata di baris tiga, bukan
"#jasadesainlogo" di blok paling bawah.

Orang Indonesia mengetik pencarian dengan bahasa sehari-hari, sering campur
Inggris dan singkatan ("kue kering lebaran", "jasa edit video murah", "outfit
kondangan"). Minta dua atau tiga frasa seperti itu dari pengguna, lalu berikan
ke linter:

```bash
python3 caption.py draf.txt --keywords "kue kering lebaran,hampers lebaran"
```

## Aturan

- **Tidak ada link di caption.** Link di caption tidak bisa diklik, termasuk
  `wa.me` dan `bit.ly`. Pindahkan ke bio, stiker link di Story, atau DM.
- **Satu ajakan.** Dua ajakan sama dengan tidak ada. `caption.py` menghitungnya.
- **Kata kunci untuk "komen ..." harus bisa diketik.** Satu kata, tanpa spasi,
  tanpa emoji, dan diucapkan juga di video. `Komen MAU` jalan.
  `Komen "aku mau template-nya kak"` tidak.
- **Jawab harga di tempat yang terlihat.** Kalau pertanyaan "harga berapa kak?"
  pasti datang, pertimbangkan menaruh harga di caption. "Cek DM" untuk harga
  bikin banyak orang pergi.
- **Kerja sama berbayar diberi label** lewat fitur Paid Partnership Instagram,
  bukan disembunyikan.
- **Emoji sebagai tanda baca, bukan hiasan.** Linter menandai lebih dari 4 per
  100 karakter.
- **Alt text layak 20 detik.** Untuk carousel dan foto, tulis. Dibaca pembaca
  layar dan oleh Instagram.

## Alurnya

1. Putuskan Tugas A atau B dan sebutkan.
2. Tulis drafnya dalam register `voice.md` (default santai).
3. Jalankan `/ig-human`. Caption pendek, jadi bahasa AI lebih nyaring di sini
   daripada di mana pun.
4. Jalankan `caption.py` dengan kata pencarian pengguna. Perbaiki semua GAGAL.
   Putuskan setiap PERIKSA secara terbuka, bukan diam-diam.
5. Cetak blok siap-salin, lalu ringkasannya:

```
CAPTION SIAP
tugas:      A - Reel-nya yang membawa hook
terlihat:   118 dari 125 karakter terpakai sebelum terpotong
ajakan:     satu, komen MAU
hashtag:    3
pencarian:  "kue kering lebaran" di baris 3, "hampers lebaran" di baris 5
linter:     SIAP
```

Tidak ada yang diposting. Pengguna yang menempelkannya.
