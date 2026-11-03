---
name: ig-reel
description: >-
  Menulis Reel Instagram berbahasa Indonesia dari ide mentah: tiga opsi hook dari
  29 formula (termasuk Ternyata, POV, Spill), naskah ucapan, teks layar, dan beat
  sheet berwaktu yang dihitung per suku kata, semuanya diskor sebelum direkam.
  Gunakan saat pengguna bilang "bikinin reels", "naskah reels", "script video
  pendek", "hook buat video", "voice over", "mau ngomong apa di video ini",
  "make a reel about X", atau mau rekam tapi belum punya kalimat pertama.
---

# ig-reel

Mengubah satu ide mentah jadi Reel yang ditonton sampai habis.

Tiga script tinggal di folder skill ini (lihat "Base directory for this skill").
Jalankan, jangan menebak hook dan jangan mengira-ngira durasi.

```bash
python3 hookscore.py hooks.txt              # urutkan opsi hook
python3 hookscore.py --hook "satu kalimat"  # skor satu hook
python3 beats.py naskah.txt --target 30     # beat sheet berwaktu
python3 beats.py naskah.txt --kalibrasi 27  # hitung laju bicara pengguna
```

`idlang.py` adalah modul bantu (suku kata, angka diucapkan). Jangan dijalankan
sendiri, tapi jangan dipisahkan dari script lain.

## Bahasa dan register

Tulis dalam bahasa Indonesia lisan, seperti orang ngomong ke kamera, bukan
bahasa tulis. Default register santai: "aku/kamu", "nggak", "udah", "banget",
campur istilah Inggris yang memang dipakai sehari-hari (posting, follow,
budget, deadline). Ikuti `voice.md` kalau ia bilang lain (gue/lo, saya/kamu,
bahasa daerah, atau formal untuk akun institusi).

Hindari bahasa terjemahan: "Anda" di akun santai, "merupakan", "tersebut",
"sebuah", "memiliki", "di era digital seperti sekarang ini". Itu langsung
terdengar seperti AI atau seperti siaran pers saat diucapkan.

## Sebelum menulis

1. Baca `~/.claude/instagram/voice.md` kalau ada. Itu profil suara pengguna:
   cara bicara di kamera, kata yang tidak pernah dipakai, kepada siapa bicara,
   dan laju bicara (suku kata per detik). Kalau belum ada, minta **tiga Reels
   atau caption mereka sendiri**, simpulkan suaranya, dan tulis file itu dari
   `voice-template.md` di folder skill ini. Naskah dengan suara yang salah
   tidak terpakai, karena harus diucapkan sendiri.
2. Baca `hooks.json` di folder ini. 29 formula, masing-masing dengan template,
   contoh, versi teks layar, kegunaan, dan cara merusaknya. #27 Ternyata,
   #28 POV dan #29 Spill adalah bentuk khas Reels Indonesia yang tidak ada di
   versi aslinya. Angka di contoh adalah ilustrasi, bukan milik pengguna.
3. Kalau idenya tipis, jangan diisi angin. Ajukan satu pertanyaan gabungan:
   apa yang terjadi, ke siapa, dan berapa ruginya atau hasilnya (dalam rupiah,
   jam, jumlah pesanan). Reel butuh satu hal spesifik yang benar.
4. Kalau `~/.claude/instagram/swipe.md` ada, baca. `/ig-viral` yang menulisnya,
   dan itu bukti pengguna sendiri soal formula yang sedang jalan di niche-nya.
   Bukti itu mengalahkan default di file ini.

## Bentuknya

Reel diputuskan di dua-tiga detik pertama dan dipertahankan lima detik
berikutnya.

```
0:00 - 0:03   HOOK        klaimnya. Kalimat ucapan dan teks layar ditulis
                          terpisah. Ada gerakan di frame pertama, bukan wajah diam.
0:03 - 0:07   TARUHAN     kenapa ini penting buat yang nonton. Satu kalimat.
0:07 - ...    ISI         satu ide per beat, dan visual berganti tiap beat.
3 dtk akhir   PEMBAYARAN  tepati janji hook, lalu satu ajakan.
BARIS AKHIR   LOOP        ulang satu kata dari hook supaya replay mulus.
```

Durasi kerja: 15 sampai 45 detik. Reels bisa sampai 3 menit dan hampir tidak
ada yang perlu. Kalimat Indonesia lebih panjang dalam suku kata daripada
padanan Inggrisnya, jadi naskah yang sama isinya cenderung beberapa detik
lebih lama. Itu alasan durasi dihitung per suku kata.

## Alurnya

**1. Pilih tiga hook, bukan satu.** Jalankan ide lewat `hooks.json`, pilih tiga
formula yang benar-benar cocok, tulis kalimat ucapan dan teks layar untuk
masing-masing. Formula berbeda, bukan tiga variasi dari satu formula.

**2. Skor.** Taruh tiga kalimat ucapan di file, satu per baris, jalankan
`hookscore.py` (pakai `--sps` dari voice.md kalau ada). Tunjukkan peringkatnya.
Kalau yang teratas di bawah 50, hook-nya belum ketemu dan tidak ada editan
yang bisa menolong. Sampaikan bahwa skor ini checklist, bukan ramalan views.

**3. Tulis naskah** dengan hook pemenang. Bahasa lisan, kalimat pendek, tanpa
kalimat yang perlu dilatih dulu sebelum bisa diucapkan. Angka ditulis dengan
cara pengguna akan mengucapkannya ("18 juta", bukan "Rp18.000.000,00").

**4. Hitung waktunya.** `beats.py naskah.txt --target {durasi} --sps {laju}`.
Perbaiki semua tanda: hook lewat 3,5 detik, beat lebih dari 4 detik, deretan
beat tanpa hal konkret, tidak ada loop. Ulangi sampai bersih. Kalau pengguna
belum pernah kalibrasi, sarankan sekali: rekam diri membaca naskah, catat
detiknya, jalankan `--kalibrasi`.

**5. Humanize.** Jalankan naskah lewat `/ig-human` sebelum ditunjukkan.

**6. Cetak bloknya.** Naskah di blok kode, teks layar sebagai daftar terpisah
dengan waktunya, lalu:

```
REEL SIAP
hook:       #3 Nggak Ada yang Bilang, skor 84 KUAT
durasi:     28,4 dtk, 9 beat, 5,5 suku kata/dtk
teks layar: 6 kartu
humanizer:  4 jejak dihapus, skor manusia 81 LULUS
caption:    lanjut ke /ig-caption

Balas "ya" untuk dicatat, atau bilang apa yang mau diubah.
```

**7. Jangan pernah publikasi.** Skill ini menghasilkan naskah. Pengguna yang
merekam dan memposting. Saat "ya", tambahkan ke `~/.claude/instagram/log.md`:
tanggal, nomor formula hook, dan kalimat pertama, supaya `/ig-audit` punya
riwayat.

## Teks layar adalah naskah terpisah

- **Maksimal enam kata per kartu.** Dibaca dari jarak sejengkal oleh orang
  yang belum mendengarkan.
- **Kartu hook muncul di frame 1**, bukan setelah jeda.
- **Di dalam safe zone.** Di frame 1080x1920, jangan ada apa pun di atas y=230
  atau di bawah y=1440, dan kosongkan 230 piksel kanan. Antarmuka Instagram
  menutupi semua di luar kotak itu.
- **Jangan taruh hook di area caption** (bawah frame). Tertutup.
- **Pasang subtitle untuk isi.** Kebanyakan orang menonton tanpa suara dulu,
  apalagi di KRL, kantor, atau kelas.

## Aturan yang membuat beda

- **Satu ide per Reel.** Kalau naskahnya punya dua, itu dua Reel. Bilang.
- **Angka di atas kata sifat.** "Rp4,2 juta" mengalahkan "lumayan banyak".
  Kalau pengguna belum memberi angka, tanya, jangan menulis di sekitar lubang.
- **Buang pembuka.** Tidak ada "Halo guys", "Assalamualaikum teman-teman", "di
  video kali ini", perkenalan nama, atau logo. Salam boleh, setelah hook. Video
  dimulai dari kalimat yang biasanya baru muncul di detik keenam.
- **Ganti visual tiap beat.** Shot diam 8 detik adalah tempat orang pergi.
- **Satu ajakan di akhir.** Komen kata kunci, simpan, atau follow. Satu.
- **Jangan pernah mengarang.** Tidak ada angka, klien, omzet atau hasil palsu
  atas nama pengguna, bahkan sebagai placeholder. Kalau butuh angka dan belum
  tahu, tulis `{{angkamu}}` dan tandai.
- **Jangan menulis naskah yang bergantung pada audio trending** yang tidak bisa
  dipakai pengguna (akun bisnis punya pustaka musik terbatas). Kalau idenya
  butuh suara pengguna sendiri, bilang.
- **Hindari SARA dan serangan ke orang tertentu.** Opini boleh tajam soal ide
  dan praktik, bukan soal suku, agama, ras, golongan, atau individu yang bisa
  dikenali. Selain etika, ada risiko hukum (UU ITE).

## Contoh

```
/ig-reel bikin penawaran harga dari 5 jam jadi 20 menit pakai satu template
```

```
HOOKS  (diskor)
  81  KUAT  #1  Pengakuan Rugi  "Empat jam seminggu aku buang cuma buat ngerapiin format."
                                teks layar: 4 JAM/MINGGU KEBUANG
  59  OKE   #5  Waktu Ringkas   "Dulu bikin penawaran harga lima jam. Sekarang dua puluh menit."
                                teks layar: 5 JAM -> 20 MENIT
  51  OKE   #9  Contek Aja      "Contek template penawaran yang bikin ini kejadian."
                                teks layar: CONTEK INI

Rekam #1: ada angka, ada yang hilang, dan kerugiannya milikmu. #5 terlemah di
SAPAAN KE: tidak bicara ke siapa-siapa. "Kamu masih butuh lima jam buat bikin
penawaran?" akan menaikkannya. #9 tidak punya satu pun hal konkret.
```
