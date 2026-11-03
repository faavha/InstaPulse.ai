---
name: ig-profile
description: >-
  Memberi skor profil Instagram dari 100 dengan rubrik 12 bagian lalu menulis
  ulang bagian yang kehilangan poin: kolom nama, bio, link, sorotan
  (highlights), tiga post yang disematkan, dan grid. Gunakan saat pengguna
  bilang "optimasi profil", "benerin bio", "nilai IG-ku", "kenapa orang nggak
  follow", "bio IG yang bagus", atau menempelkan profilnya dan bertanya
  kesannya.
---

# ig-profile

Hampir semua orang mengoptimasi hal yang salah di sini. Profil bukan etalase
yang dijelajahi. Profil adalah **layar keputusan**, didatangi dari satu Reel,
dan punya sekitar tiga detik untuk menjawab satu pertanyaan: ada lagi yang
seperti tadi di sini, dan apakah ini untukku.

## Input

Minta pengguna menempelkan atau screenshot: kolom nama, handle, bio, tujuan
link, nama-nama sorotan, apa yang disematkan, dan sembilan cover grid pertama.
Screenshot bagian atas profil plus dua baris grid pertama cukup untuk putaran
pertama.

Jangan login ke Instagram atas nama pengguna.

## Beri skor

Baca `rubric.json` di folder ini. Dua belas item, 100 poin, masing-masing
dengan seperti apa nilai penuh dan cara gagal yang paling umum. Nilai setiap
item, tunjukkan tabelnya, beri totalnya. Jujur. Kebanyakan profil mendapat
30-an dan 40-an di putaran pertama, dan skor yang murah hati tidak berguna.

```
SKOR PROFIL  38/100

  kolom nama        2/12   cuma nama, tidak ada kata yang dicari orang
  baris 1 bio       3/12   "Pejuang rupiah | Pecinta kopi | Anak mama ☕"
  tiga sematan      0/10   tidak ada yang disematkan
  sorotan           2/8    "Random", "Me", "2023"
  grid terbaca      4/8    enam dari sembilan cover wajah lagi ngomong
  ...
```

## Lalu tulis ulang, dengan urutan ini

Perbaiki dari yang paling banyak kehilangan poin. Jangan tulis ulang semuanya
sekaligus, pengguna harus benar-benar pergi mengubah tiap bagian.

**1. Kolom nama (30 karakter).** Baris tebal di bawah foto, bukan handle. Ini
kolom yang dicocokkan pencarian Instagram, dan kebanyakan akun hanya mengisinya
dengan nama. Format yang jalan: `{Nama} | {pekerjaan, dengan kata yang dicari}`.
Pakai kata yang diketik orang Indonesia saat mencari: "Jasa Desain Logo",
"Katering Solo", "Les Matematika SMP", bukan "Creative Visual Storyteller".
Beri tiga opsi.

**2. Baris pertama bio.** Untuk siapa ini dan apa yang berubah buat mereka.
Bukan jabatan, bukan kata sifat, bukan daftar identitas dipisah garis tegak.
Sisa 150 karakter membawa satu bukti atau satu tawaran yang jelas (area
layanan atau kota boleh, karena orang mencari "... Jogja", "... Surabaya").

**3. Tiga sematan.** Tiga slot, tiga tugas berbeda: bukti terbaik, penjelasan
penawaran yang paling jelas, perkenalan terbaik tentang orangnya. Ini perbaikan
dengan daya ungkit tertinggi di seluruh profil dan cuma butuh empat ketukan.

**4. Sorotan.** Empat sampai enam, dinamai dengan pertanyaan yang ditanyakan
pembeli: Harga, Testimoni, Cara Order, Tentang. Bukan "Random". Hapus sisanya.
Testimoni hanya yang asli dan dengan izin; sensor nama dan nomor pembeli.

**5. Link.** Satu tujuan yang cocok dengan janji bio. Link WhatsApp (`wa.me`)
wajar dan sering terbaik untuk bisnis lokal, asalkan ada pesan pembuka yang
sudah terisi. Lima link diizinkan; dua saja sudah jadi menu, dan menu
mengonversi lebih buruk daripada pintu.

**6. Cover grid.** Sembilan pertama di ukuran thumbnail. Cover Reel dipilih,
bukan dibiarkan frame pertama. Empat kata di cover membuat grid terbaca sekali
lirik.

## Output

Tabel skor, lalu tulisan ulang sebagai blok siap-salin dengan urutan perbaikan,
masing-masing lewat `/ig-human`. Nilai ulang di akhir dan tunjukkan selisihnya
dengan jujur. Kalau tulisan ulangnya mencapai 84 dan bukan 98, bilang 84, dan
bilang apa yang dibutuhkan sisanya, biasanya grid, kebiasaan story, dan post
sematan yang belum ada. Semua itu bukan tulisan ulang.

Skill ini tidak menyimpan apa pun ke Instagram. Pengguna yang mengedit tiap kolom.
