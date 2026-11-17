# Website PCM Banjarsari (Django)

Tugas 1 — Pemrograman Web berbasis Framework (TIF1336): membangun dan men-deploy website untuk
**Pimpinan Cabang Muhammadiyah (PCM) Banjarsari, Kota Surakarta** dengan Django, Docker, dan PostgreSQL.

> Website ini dibuat untuk tugas kuliah dan **bukan website resmi** PCM Banjarsari.

## Kelompok

| Nama | NIM |
|------|-----|
| _Danar Tri Prayoga_ | _L200240185_ |
| _Daffa Raihan_ | _L200240203_ |
| _Azwar Dipo Astuko_ | _L200240173_ |
| _Gibran Alghifari Maulana Masli_ | _L200240172_ |
| _Kaukaban Syarqi_ | _L200240176_ |

**Nama kelompok:** PCM Banjarsari

## PCM yang dipilih

- **PCM Banjarsari**, Kecamatan Banjarsari, Kota Surakarta, Jawa Tengah (PDM Kota Surakarta, PWM Jawa Tengah).
- Sekretariat: Jl. KH. Ahmad Dahlan No. 35, Keprabon, Surakarta, telp. 0271-667533 (kontak resmi sekretariat dari kop surat PCM).
- **Pengurus yang memberi izin:** _isi nama dan jabatan pengurus PCM Banjarsari yang mengizinkan data/foto dipakai_.

## Sumber data

| Data | Sumber | Tanggal diambil |
|------|--------|-----------------|
| Susunan pimpinan 2022–2027 | SK PCM Banjarsari No. 157/KEP/IV.0/D/2023 (21 Okt 2023) dan SK PDM Kota Surakarta No. 128/KEP/III.0/D/2023 | _isi_ |
| Sejarah dan SK pendirian cabang | SK PWM Jawa Tengah No. K/79/1978 (24 Muharram 1398 H / 4 Jan 1978 M) | _isi_ |
| Daftar ranting, SK pendirian ranting, jumlah anggota ber-NBM (513) | Laporan Musyawarah Cabang Muhammadiyah Banjarsari 2023, hlm. 9 (angka periode 2015–2022) | _isi_ |
| Ketua ranting Keprabon, Timuran, Punggawan, Kestalan | SK PCM No. 168, 174, 171, 169/KEP/IV.0/D/2023 (25 Des 2023) | _isi_ |
| Ketua ranting Ketelan dan Gilingan | SK PCM No. 018/KEP/IV.0/D/2026 (26 Jun 2026) dan No. 029/KEP/IV.0/D/2026 (9 Okt 2026) | _isi_ |
| Ketua ranting Setabelan | **Belum tersedia** (SK belum diterima), ditulis "Belum tersedia" | - |
| Amal usaha (SMA Muhammadiyah 6, 9 masjid, Wisma Musolla Pemuda) | Laporan Musycab 2023 hlm. 12; berkas "amal usaha pcm banjarsari"; papan "Tanah Milik Muhammadiyah" di lokasi | _isi_ |
| Berita dan agenda koordinasi 16 Okt 2026 | Poster dan contoh publikasi "PCM Banjarsari News" dari pengurus | _isi_ |
| Agenda Pengajian Hari Bermuhammadiyah (25 Okt) dan Safari Dakwah (rencana Des–Jan, belum pasti) | Berkas "kegiatan mendatang pcm banjarsari" | _isi_ |
| Kegiatan rutin (rapat pleno, pengajian HPT, dll.) | Berkas "kegiatan rutin pcm banjarsari" | _isi_ |
| Visi dan misi | Berkas "visi misi muhammadiyah" | _isi_ |
| Tagline "Memajukan Banjarsari, Mencerahkan Semesta." | Sampul/footer dokumen Musycab 2023 | _isi_ |
| Tautan PDM, PWM, PP | muhammadiyahsolo.com (tercantum di kop PDM Kota Surakarta), pwmjateng.com, muhammadiyah.or.id | _isi_ |

### Catatan data

- Tidak ada nomor HP pribadi, alamat rumah, NIK, atau NBM pengurus yang ditampilkan.
- Data yang tidak ada (email sekretariat, alamat dan telepon ranting, ketua PRM Setabelan, foto pimpinan, dokumen unduhan) dikosongkan atau ditulis "Belum tersedia".
- Angka **513 anggota ber-KTAM** adalah data Musycab 2023 (periode 2015–2022). Perbarui lewat admin bila ada angka terbaru.
- Foto (hero, sampul berita, foto pimpinan, gambar amal usaha) tidak disertakan; unggah sendiri lewat admin.

## Teknologi

Python 3.12+ (Docker memakai 3.14), Django 6.x, uv, template Django (server-side), CSS buatan sendiri,
SQLite (laptop) / PostgreSQL (produksi), WhiteNoise, Gunicorn, django-storages (S3-compatible) untuk media.

## Menjalankan di laptop (uv)

```bash
uv sync
cp .env.example .env          # lalu isi; di laptop cukup DEBUG=True
uv run python manage.py migrate
uv run python manage.py seed_pcm
uv run python manage.py createsuperuser
uv run python manage.py runserver
# buka http://127.0.0.1:8000  dan  http://127.0.0.1:8000/admin/
```

Test: `uv run python manage.py test`

**Logo (wajib):** unduh [Muhammadiyah.svg](https://commons.wikimedia.org/wiki/File:Muhammadiyah.svg) dari Wikimedia Commons
**tanpa diubah**, simpan sebagai `static/img/logo-muhammadiyah.svg`, lalu commit. Atribusi CC BY-SA 4.0 sudah ada di footer.

## Menjalankan dengan Docker

```bash
docker compose up --build
# buka http://localhost:8000
docker compose exec web uv run python manage.py seed_pcm
docker compose exec web uv run python manage.py createsuperuser
```

- Database PostgreSQL 17 berjalan di service `db` (volume `postgres_data`, `healthcheck` `pg_isready`).
  Port database tidak dibuka ke host, sehingga tidak ada password yang disimpan di repo.
- `web` menunggu `db` sehat, menjalankan `migrate`, lalu Gunicorn. `SECRET_KEY` dibuat acak jika tidak ada di `.env`.
- Gambar unggahan disimpan di volume `media_data`, sehingga tetap ada setelah `docker compose down` lalu `up`.
- `docker compose down -v` **menghapus volume** (database dan gambar) sehingga semuanya kembali kosong. Gunakan hanya untuk mengulang dari awal.

## Deployment

- **Platform:** _isi (Vercel / Render / Railway)_ — alasan: _isi_
- **Database:** _isi (Supabase / Neon)_ — alasan: _isi_
- **Object storage media:** _isi (mis. Supabase Storage via S3)_ — alasan: _isi_
- **URL produksi:** _isi_

Langkah ringkas: atur environment variable di dashboard platform, jalankan
`DATABASE_URL=<url produksi> uv run python manage.py migrate` lalu `... seed_pcm` dari laptop, dan buat superuser.
Jika memakai pooler mode transaction (Supabase port 6543 atau Neon "-pooler"), set `DB_TRANSACTION_POOLER=True`.
Untuk migrasi di Neon, pakai koneksi *direct*.

## Environment variable

Lihat [`.env.example`](.env.example): `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `DATABASE_URL`,
`DB_TRANSACTION_POOLER`, dan `AWS_*` untuk object storage.

## Struktur singkat

```
config/        settings, urls, wsgi
web/           models (+custom QuerySet), views, forms, admin, context processor, tests
web/management/commands/seed_pcm.py   data riil PCM (tanpa gambar)
templates/     base.html, 404.html, web/*.html (+ _kartu_berita, _item_agenda)
static/css/    site.css
```

## Kontribusi anggota

| Anggota | Dikerjakan |
|---------|------------|
| _isi_ | _isi_ |
| _isi_ | _isi_ |

## Akun admin demo

Dikirim terpisah ke dosen, tidak di-commit.

## Lisensi dan atribusi

Logo Muhammadiyah: K. H. Siradj Dahlan, vektor oleh Hibensis, via Wikimedia Commons, lisensi CC BY-SA 4.0.
