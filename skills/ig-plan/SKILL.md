---
name: ig-plan
description: >-
  Menyusun rencana Instagram seminggu untuk akun Indonesia: apa yang diposting,
  format apa, jam berapa (WIB/WITA/WIT), dan dengan siapa berinteraksi. Gunakan
  saat pengguna bilang "rencanain minggu ini", "jadwal konten", "kalender
  konten", "posting apa ya", "bingung mau posting apa", "content plan", atau
  ingin jadwal posting dan daftar akun untuk engagement.
---

# ig-plan

Ruang kendali. Semua skill lain di paket ini mengeksekusi; yang ini memutuskan
apa yang dieksekusi. Jalankan sekali seminggu, di hari yang sama.

## Input

Kalau `~/.claude/instagram/voice.md`, `swipe.md` dan `log.md` ada, baca. Swipe
file adalah bukti pengguna sendiri dari `/ig-viral` soal formula yang sedang
jalan di niche-nya, dan itu mengalahkan apa pun di file ini. Log mencegah
rencana mengulang tema dua minggu terakhir.

Kalau belum ada, tanya empat hal dan catat:

1. Apa yang dijual pengguna, dan ke siapa.
2. Tiga atau empat tema yang ingin membuatnya dikenal.
3. Apa yang benar-benar terjadi minggu ini: obrolan dengan klien, satu angka,
   satu kesalahan, sesuatu yang dibuat, satu perdebatan. Dari sinilah post
   datang.
4. Sepuluh akun yang layak melihatnya.

## Apa yang diposting

Empat sampai lima post seminggu, minimal tiga di antaranya Reels. Reels adalah
satu-satunya format di Instagram yang secara konsisten menjangkau orang yang
belum follow. Carousel masuk dalam ke orang yang sudah follow. Story harian dan
direncanakan terpisah.

Campur sepanjang minggu, jangan pernah dua jenis yang sama berturut-turut:

| jenis | porsi | tugas |
| --- | --- | --- |
| **Bukti** | 1 per minggu | sesuatu yang terjadi, dengan angka. Reel. |
| **Ajar** | 1-2 per minggu | satu hal yang bisa dilakukan penonton hari ini. Reel atau carousel. |
| **Opini** | 1 per minggu | sikap yang bisa bikin sebagian follower pergi. Reel. |
| **Cerita** | 1 per dua minggu | adegan dengan harga yang dibayar. Reel. |
| **Tawaran** | 1 per dua minggu | apa yang dijual, terang-terangan, tanpa minta maaf. Carousel atau story. |

Untuk tiap slot, beri: tema, sudut spesifik dari apa yang terjadi minggu ini,
format, dan nomor formula hook dari `ig-reel/hooks.json`. Bukan topik, sudut.
"AI" bukan rencana. "Klien yang batal karena proposal kita kelihatan ditulis
ChatGPT" adalah Reel.

**Opini yang tajam soal ide dan praktik, bukan soal orang atau SARA.** Hindari
menyerang individu yang bisa dikenali, suku, agama, ras, atau golongan. Selain
soal etika, ada risiko hukum (UU ITE).

## Kalender lokal

Cek apakah minggu ini bersinggungan dengan momen yang menggeser perilaku
audiens Indonesia, dan sesuaikan sudutnya, bukan hanya jam posting:

- **Gajian** (sekitar tanggal 25 sampai awal bulan): niat beli naik, cocok untuk
  slot Tawaran.
- **Ramadan**: jam aktif bergeser ke sahur dan menjelang buka (ngabuburit) serta
  setelah tarawih; konten THR, mudik, hampers dan Lebaran.
- **Harbolnas 11.11 dan 12.12, tanggal kembar lain**: musim promo marketplace.
- **Libur panjang, tahun ajaran baru, akhir tahun.**

Jangan mengarang tanggal momen yang bergerak (awal Ramadan, Idulfitri). Kalau
tidak yakin, cari dulu atau tanya pengguna.

## Kapan posting

Posting saat audiens bangun dan tidak sedang sibuk bekerja, dalam **zona waktu
audiens** (WIB, WITA, atau WIT), bukan zona waktu pengguna kalau beda. Titik
awal yang masuk akal untuk audiens konsumen Indonesia: jam istirahat siang
(sekitar 12.00-13.00) dan malam setelah makan malam (sekitar 19.00-21.00).
Audiens bisnis atau profesional: pagi sebelum jam kerja dan perjalanan pulang.
Hari Jumat siang banyak audiens laki-laki muslim sedang salat Jumat. Ini titik
awal, bukan aturan: insight akun pengguna sendiri (kapan follower aktif) selalu
menang.

Tapi katakan ini dengan jelas: **jamnya jauh kurang penting daripada dua detik
pertama.** Instagram akan terus menampilkan Reel berhari-hari kalau
performanya bagus, dan mengubur yang jamnya tepat tapi hook-nya lemah. Kalau
pengguna sibuk mengoptimasi jam posting sebelum hook-nya jalan, mereka memoles
hal yang salah, dan kamu harus bilang.

## Putaran engagement, yang tidak opsional

20 menit sehari, sebelum posting, bukan sesudah. Susun daftar 10:

- **5 jangkauan** - akun dengan audiens yang diinginkan pengguna, tempat komen
  bagus akan terlihat. Komen lebih awal, sebelum thread-nya 200 komen.
- **3 sejawat** - ukuran sama, bidang sama. Kelompok yang membalas budi.
- **2 pembeli** - orang yang benar-benar bisa membeli. Komen berminggu-minggu
  sebelum DM apa pun, dan jangan pernah jualan di kolom komen.

Serahkan daftarnya ke `/ig-comment`.

## Output

```
MINGGU 16 NOV  ·  zona audiens: WIB

SEN  engage saja  (20 menit, daftar di bawah)
SEL  19.30  REEL      BUKTI    #5  Waktu Ringkas    - penawaran 5 jam jadi 20 menit
RAB  story saja + engage
KAM  12.15  CAROUSEL  AJAR     caption Tugas B      - bedah 4 pasal kontrak
JUM  19.30  REEL      OPINI    #2  Perintah Larangan - stop kasih diskon ke teman
SAB  -
MIN  19.00  REEL      CERITA   #21 Mulai di Tengah  - email minta refund itu

STORY  tiap hari, 3-5 frame, kotak pertanyaan hari Kamis.
MOMEN  gajian mulai 25 Nov: geser slot Tawaran ke Selasa depan.

ENGAGE  (5 jangkauan / 3 sejawat / 2 pembeli)
  ...

Bilang "tulis Selasa" dan aku buatkan drafnya.
```

Tulis rencana ke `~/.claude/instagram/plan.md` supaya skill lain bisa
membacanya. Tidak ada yang dijadwalkan atau diposting di mana pun. Ini rencana
dan pengguna yang menjalankannya.
