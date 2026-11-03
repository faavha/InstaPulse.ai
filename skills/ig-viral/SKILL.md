---
name: ig-viral
description: >-
  Mencari Reels yang benar-benar sedang jalan di niche pengguna, mengurutkannya
  berdasarkan seberapa jauh tiap Reel mengalahkan akunnya sendiri (outlier
  multiple), menamai formula hook-nya, dan mengubahnya jadi swipe file yang
  siap direkam. Gunakan saat pengguna bilang "cari video viral", "apa yang lagi
  rame", "konten apa yang jalan di niche-ku", "bedah akun ini", "bikin swipe
  file", "kenapa reels ini meledak", atau bingung mau bikin apa dan belum punya
  bukti.
---

# ig-viral

Skill riset. Semua skill lain di paket ini menulis; yang ini pergi melihat.
Jalankan sebulan sekali, bukan tiap hari. Formula bertahan satu musim.

Satu script tinggal di folder skill ini:

```bash
python3 swipe.py tangkapan.tsv --out ~/.claude/instagram/swipe.md
```

Script ini mengimpor `hookscore.py` dan `hooks.json` dari folder `ig-reel`,
jadi dua skill ini harus terpasang bersama.

## Satu ide yang membuat ini layak

**Views mentah bukan bukti.** Akun 2 juta follower dapat 400 ribu views itu
sedang sepi. Akun 4 ribu follower dapat 400 ribu views menemukan sesuatu, dan
sesuatu itu bisa ditiru.

Jadi semuanya diurutkan berdasarkan **outlier multiple**: views dibagi median
views akun itu sendiri. Di atas 3x itu sinyal. Di bawah 1,5x itu hari biasa akun
tersebut dan tidak mengajarkan apa pun, sebesar apa pun angkanya.

Kumpulkan akun yang **ukurannya dalam kisaran 10x dari akun pengguna**. Formula
yang jalan di 2 juta follower sering jalan karena 2 juta follower-nya.

## Langkah 1: pilih akunnya

Minta 6 sampai 12 akun dari pengguna, atau usulkan lalu minta persetujuan:

- **4 langsung** - niche sama, penawaran sama, sedikit di depan.
- **4 bersebelahan** - niche beda, audiens sama. Di sinilah format dipinjam
  sebelum ada yang memakainya di niche pengguna.
- **2 sampai 4 raksasa** - akun jauh lebih besar, untuk format saja, bukan
  frekuensi atau nada.

Prioritaskan akun Indonesia: bahasanya, humornya, dan kebiasaan penontonnya
sama dengan audiens pengguna. Akun luar negeri bagus untuk format, bukan untuk
naskah.

Minta juga pengguna membuka **koleksi Tersimpan (Saved)** miliknya. Itu korpus
tercepat dan paling relevan yang ada, sudah tersaring oleh seleranya sendiri.

## Langkah 2: pergi melihat

Pakai alat browsing apa pun yang benar-benar ada di sesi ini: browser di dalam
aplikasi, ekstensi browser yang terhubung ke Chrome pengguna, atau computer use.
Tidak ada API untuk ini dan tidak perlu, volumenya cukup kecil untuk dibaca.

**Aturan yang tidak bisa ditawar:**

- **Jangan pernah login ke Instagram atas nama pengguna dan jangan pernah minta
  password.** Kalau halaman butuh login, pengguna yang sudah login. Kendalikan
  browser mereka dengan mereka hadir, atau minta mereka menempelkan datanya.
- **Ini membaca, bukan scraping.** Sepuluh akun, selusin Reels masing-masing,
  dengan kecepatan manusia. Pengumpulan otomatis dalam jumlah besar melanggar
  Ketentuan Penggunaan Instagram dan membuat akun dibatasi. Jangan membuat
  crawler, jangan pakai jasa scraping, jangan dijalankan berulang di latar.
- **Tiru formulanya, jangan videonya.** Bentuk hook, struktur, durasi, pola
  potongan. Bukan naskahnya, suaranya, atau editannya. Cantumkan akun asal di
  setiap baris swipe file.

**Yang dicatat per Reel**, dengan kata-kata kreatornya sendiri:

| kolom | catatan |
| --- | --- |
| account (akun) | handle |
| followers (pengikut) | dari profil |
| median | lihat 12 Reels terakhir, ambil views yang di tengah |
| views (tayangan) | Reel ini |
| hook | kalimat pertama, diucapkan atau di layar, persis, termasuk salah ketik dan bahasa gaulnya |
| on-screen | kartu teks pertama, kalau berbeda |
| length | detik |
| cta | apa yang diminta di akhir |

Angka boleh ditulis persis seperti tampilan Instagram berbahasa Indonesia:
`412rb`, `1,2jt`, `48.000`. Script membacanya dengan benar. Header kolom boleh
bahasa Indonesia (akun, pengikut, tayangan).

Median yang paling penting. Tanpa median kamu kembali mengurutkan berdasarkan
jumlah follower, hal yang ingin dihentikan skill ini.

**Kalau Instagram tidak menunjukkan cukup banyak:** tata bahasa hook yang sama
jalan di YouTube Shorts, yang jumlah views dan transkripnya publik tanpa login.
Itu korpus kedua yang sah:

```bash
# views shorts satu channel
python3 -m yt_dlp --flat-playlist --playlist-end 40 -J \
  "https://www.youtube.com/@HANDLE/shorts" > channel.json

# kalimat pertama satu short, dari subtitle otomatis bahasa Indonesia
python3 -m yt_dlp --skip-download --write-auto-subs --sub-langs "id.*" \
  --sub-format json3 -o hook "https://www.youtube.com/watch?v=VIDEO_ID"
```

Ambil semua kata subtitle dengan timestamp di bawah 3,0 detik. Itulah hook-nya,
seperti diucapkan, bukan seperti ditulis. (Jaringan sesi ini mungkin memblokir
YouTube; kalau begitu, bilang dan minta pengguna menjalankannya sendiri.)

TikTok juga korpus yang sah untuk audiens Indonesia, karena banyak format
pindah dari TikTok ke Reels. Baca dengan aturan yang sama: manual, kecepatan
manusia, tanpa login atas nama pengguna.

## Langkah 3: urutkan

Isi file dipisah TAB dengan baris judul, lalu jalankan script:

```
akun	pengikut	median	tayangan	hook
@akun	48rb	11rb	412rb	nggak ada yang bilang 30 reels pertama bakal sepi
```

```bash
python3 swipe.py tangkapan.tsv --out ~/.claude/instagram/swipe.md
```

Script menghitung outlier multiple, menamai formula hook memakai 29 formula
yang sama dengan `/ig-reel`, memberi skor tiap hook dengan `hookscore.py`, dan
mencetak apa yang membedakan sepertiga teratas dari sepertiga terbawah.

## Langkah 4: katakan artinya, hati-hati

Laporkan tiga hal, tidak lebih:

1. **Formula mana yang menonjol** di sepertiga teratas, dengan jumlahnya. Dua
   formula muncul masing-masing empat kali di enam akun itu temuan. Satu muncul
   dua kali bukan.
2. **Kesamaan struktural sepertiga teratas** yang tidak dimiliki sepertiga
   terbawah: panjang hook, apakah hasilnya visual, apakah frame pertama
   bergerak, di mana ajakannya.
3. **Baris yang belum terklasifikasi.** Setiap hook yang tidak bisa dinamai
   classifier itu noise atau formula yang belum ada di `hooks.json`. Baca
   manual. Ini kolom paling berharga dan alasan script mencetak jumlahnya.
   Kalau menemukan bentuk baru yang berulang, tawarkan untuk menambahkannya ke
   `hooks.json` (id baru, template, contoh, regex `match`).

Lalu sebutkan ukuran sampel dan tingkat keyakinan dengan kata-kata biasa. Empat
puluh Reels dari enam akun mendukung sebuah klaim. Dua belas tidak, dan
mengatakannya adalah beda antara riset dan ramalan zodiak.

## Langkah 5: ubah jadi sesuatu yang bisa direkam

Untuk tiga formula teratas, tulis **versi pengguna**: cerita mereka sendiri,
angka mereka sendiri, dalam bentuk yang sedang jalan. Serahkan masing-masing ke
`/ig-reel` dengan id formula sudah dipilih.

Jangan pernah menyerahkan "bikin reels kayak gini". Serahkan kalimat hook yang
bisa mereka ucapkan besok.

## Output

```
SWIPE  ·  38 reels  ·  7 akun  ·  baseline: median akun

OUTLIER (di atas 3x)
  38.4x  hook 84  #3  Nggak Ada yang Bilang  @akun_a    412.000  (median 10.700)
  11.2x  hook 79  #28 POV                    @akun_c    180.000  (median 16.100)
  ...

YANG MENONJOL
  #3 Nggak Ada yang Bilang   x5 di sepertiga atas, 0 di bawah
  #2 Perintah Larangan       x4
  median panjang hook        8 kata di atas, 17 di bawah

BELUM TERKLASIFIKASI (6)
  Dua di antaranya bentuknya sama dan belum ada di hooks.json: hook yang
  dibuka dengan membacakan komentar orang lain. Layak ditambahkan.

VERSIMU
  #3  "Nggak ada yang bilang kalau 20 penawaran pertamamu memang bakal ditolak."
  ...
```

(Angka di atas ilustrasi format, bukan data.)

Tulis swipe file ke `~/.claude/instagram/swipe.md`. `/ig-reel` dan `/ig-plan`
sama-sama membacanya, itulah intinya: setelah ini jalan sekali, seluruh paket
bekerja dari bukti pengguna sendiri, bukan dari default.

Skill ini tidak memposting, mem-follow, me-like, atau mengirim pesan apa pun.
Ia membaca.
