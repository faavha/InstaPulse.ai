---
name: ig-audit
description: >-
  Bedah post-mortem konten Instagram yang sudah diposting pengguna: Reels mana
  yang benar-benar berhasil, kenapa, dan apa yang harus berhenti dibuat. Bisa
  membaca screenshot Insights versi bahasa Indonesia maupun Inggris. Gunakan
  saat pengguna menempelkan Insights atau daftar post lalu bertanya "apa yang
  jalan", "kenapa reels ini sepi", "baca analitikku", "audit kontenku", atau
  ingin tahu apa yang harus diperbanyak.
---

# ig-audit

Satu-satunya sumber jujur soal apa yang jalan untuk sebuah akun adalah akun itu
sendiri. Setiap aturan di setiap panduan Instagram, termasuk di paket ini,
adalah dugaan awal. 30 post terakhir pengguna adalah buktinya.

## Input

Minta yang dimiliki pengguna:

- Insights per post: views (tayangan), jangkauan (akun yang dijangkau),
  interaksi, waktu tonton, simpan, bagikan, follow, dan porsi jangkauan dari
  non-follower. Screenshot boleh.
- Atau grafik retensi Reels terbaik dan terburuk. Satu screenshot ini lebih
  berharga daripada semua yang lain digabung.
- Atau hanya post-nya dan jumlah views-nya, cukup untuk putaran pertama.

Label Insights berbeda tergantung bahasa aplikasi dan versi. Petakan ke metrik
di bawah berdasarkan artinya, bukan namanya; kalau ragu label tertentu artinya
apa, tanya pengguna daripada menebak. Angka bisa tampil sebagai "12,4 rb" atau
"1,2 jt"; baca koma sebagai desimal.

Baca juga `~/.claude/instagram/log.md` kalau ada, karena mencatat formula hook
yang dipakai tiap post.

## Apa yang sebenarnya diukur

Views mentah adalah angka paling tidak berguna di halaman itu, karena sebagian
besar ditentukan jumlah follower. Hitung ini dan tunjukkan perhitungannya:

| metrik | cara | yang diceritakan |
| --- | --- | --- |
| **Outlier multiple** | views / median views akun sendiri | hit beneran atau hari biasa |
| **Jangkauan non-follower** | % jangkauan dari yang tidak follow | apakah menyebar sama sekali |
| **Bertahan di 3 dtk** | penonton di detik 3 / yang mulai menonton | apakah hook-nya jalan. Ini rapor hook. |
| **Rata-rata waktu tonton** | langsung dari Insights | apakah bagian tengahnya jalan |
| **Kirim per jangkauan** | bagikan / jangkauan | sinyal terkuat yang bisa didapat. Kiriman adalah orang yang mempertaruhkan namanya. |
| **Follow per jangkauan** | follow / jangkauan | apakah profil mengubah perhatian jadi follower |

Urutkan berdasarkan outlier multiple dan kirim per jangkauan, bukan views. Reel
dengan 4.000 views dan 90 kiriman mengalahkan yang 60.000 views dan 11 kiriman.

Kerjakan hitungannya dengan kode, bukan di kepala, kalau datanya lebih dari
segelintir post.

## Lalu cari polanya

Dengan lima teratas dan lima terbawah berdampingan, cari apa yang memisahkan
mereka, dan berani menyimpulkan sesuatu yang tidak disukai pengguna:

- **Bertahan di 3 detik.** Kalau atas dan bawah berbeda di sini, masalahnya hook
  dan bukan yang lain, dan semua yang di hilir hanya pengalih perhatian.
- **Formula hook.** Id mana dari `ig-reel/hooks.json` yang ada di lima teratas?
- **Format.** Reel, carousel, satu gambar.
- **Durasi.** Kelompokkan: di bawah 15 dtk, 15-30, 30-60, di atas 60.
- **Tema.**
- **Bahasa dan register.** Apakah yang santai mengalahkan yang formal, atau
  sebaliknya? Campur Inggris atau tidak?
- **Apakah pengguna membalas komen di jam pertama.**
- **Hari dan jam.** Periksa **paling akhir** dan hanya kalau yang lain tidak
  menunjukkan apa-apa. Hampir tidak pernah penyebabnya, dan justru di situ orang
  ingin penyebabnya berada. Pengecualian yang wajar dicek: momen seperti
  gajian, Ramadan, atau Harbolnas.

Sampaikan temuan sebagai klaim dengan buktinya, dan sebutkan seberapa yakin.
Dengan 30 post kamu bisa melihat pola. Dengan 6 tidak bisa, dan mengatakannya
lebih baik daripada mengarang satu.

## Perbedaan yang menghemat berbulan-bulan

**Reel yang dapat views tapi tidak dapat follow bukan Reel gagal, itu masalah
profil.** Reel yang tidak dapat views adalah masalah hook. Pisahkan keduanya
sebelum merekomendasikan apa pun. Kalau jangkauan non-follower tinggi dan follow
per jangkauan rendah, berhenti menulis ulang hook dan pergi ke `/ig-profile`.

## Output

```
AUDIT  ·  31 post  ·  12 Jun - 5 Sep  ·  median views 4.100

5 TERATAS BERDASARKAN OUTLIER MULTIPLE
  18.2x  #3  Nggak Ada yang Bilang  74.600 views  62% non-follower  bertahan@3s 71%  128 kirim
   6.4x  #1  Pengakuan Rugi         26.300 views  48% non-follower  bertahan@3s 64%   71 kirim
  ...

5 TERBAWAH
   0.3x  #11 Bernomor               1.200 views    9% non-follower  bertahan@3s 31%    2 kirim
  ...

KATA DATANYA
1. Bertahan di 3 detik adalah seluruh ceritanya. Lima teratas rata-rata 66%,
   lima terbawah 33%. Semua yang kamu khawatirkan ada di hilir dua detik pertama.
2. Post di mana kamu yang kelihatan salah: rata-rata 8,1x vs 0,9x untuk yang
   lain. n=5. Sinyal terkuat di sini, dan jauh.
3. Listicle aplikasi dapat views dan tidak dapat apa-apa lagi. Jangkauan tinggi,
   tanpa kiriman, tanpa follow. Tiga dari lima terbawah.
4. Hari posting tidak menunjukkan apa-apa. Rata-rata Selasa dan Jumat-mu ada di
   dalam noise. Berhenti mengoptimasinya.

STOP: listicle.
PERBANYAK: yang ada harga yang kamu bayar dan angkanya.
```

(Angka di atas ilustrasi format, bukan data.)

Lalu serahkan kesimpulannya ke `/ig-plan` supaya minggu depan dibangun di atas
bukti pengguna sendiri, dan ke `/ig-viral` supaya swipe file disaring ke
formula yang jalan untuk akun ini secara khusus.
