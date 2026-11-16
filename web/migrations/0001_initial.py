import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Profil",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nama", models.CharField(max_length=200)),
                ("nama_singkat", models.CharField(max_length=60)),
                ("tagline", models.CharField(blank=True, max_length=200)),
                ("tentang", models.TextField(blank=True)),
                ("sejarah", models.TextField(blank=True)),
                ("visi", models.TextField(blank=True)),
                ("misi", models.TextField(blank=True, help_text="Satu misi per baris.")),
                ("alamat_sekretariat", models.CharField(blank=True, max_length=300)),
                ("telepon", models.CharField(blank=True, max_length=40)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("jumlah_anggota_ktam", models.PositiveIntegerField(default=0)),
                ("gambar_hero", models.ImageField(blank=True, upload_to="hero/")),
            ],
            options={
                "verbose_name": "Profil organisasi",
                "verbose_name_plural": "Profil organisasi",
            },
        ),
        migrations.CreateModel(
            name="Pimpinan",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nama", models.CharField(max_length=200)),
                ("jabatan", models.CharField(max_length=120)),
                ("periode", models.CharField(default="2022–2027", max_length=20)),
                ("foto", models.ImageField(blank=True, upload_to="pimpinan/")),
                ("urutan", models.PositiveIntegerField(default=0)),
            ],
            options={
                "verbose_name": "Pimpinan",
                "verbose_name_plural": "Pimpinan",
                "ordering": ["urutan", "id"],
            },
        ),
        migrations.CreateModel(
            name="Ranting",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nama", models.CharField(max_length=120)),
                ("ketua", models.CharField(blank=True, max_length=200)),
                ("alamat", models.CharField(blank=True, max_length=300)),
                ("telepon", models.CharField(blank=True, max_length=40)),
            ],
            options={
                "verbose_name": "Ranting",
                "verbose_name_plural": "Ranting",
                "ordering": ["nama"],
            },
        ),
        migrations.CreateModel(
            name="AmalUsaha",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nama", models.CharField(max_length=200)),
                (
                    "bidang",
                    models.CharField(
                        choices=[
                            ("pendidikan", "Pendidikan"),
                            ("kesehatan", "Kesehatan"),
                            ("sosial", "Sosial"),
                            ("ekonomi", "Ekonomi"),
                        ],
                        max_length=20,
                    ),
                ),
                ("deskripsi", models.TextField(blank=True)),
                ("alamat", models.CharField(blank=True, max_length=300)),
                ("gambar", models.ImageField(blank=True, upload_to="amal-usaha/")),
            ],
            options={
                "verbose_name": "Amal usaha",
                "verbose_name_plural": "Amal usaha",
                "ordering": ["bidang", "nama"],
            },
        ),
        migrations.CreateModel(
            name="Berita",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("judul", models.CharField(max_length=250)),
                ("slug", models.SlugField(blank=True, max_length=250, unique=True)),
                ("ringkasan", models.TextField(max_length=500)),
                ("isi", models.TextField()),
                ("gambar_sampul", models.ImageField(blank=True, upload_to="berita/")),
                ("tanggal_terbit", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "status",
                    models.CharField(
                        choices=[("draf", "Draf"), ("terbit", "Terbit")],
                        default="draf",
                        max_length=10,
                    ),
                ),
            ],
            options={
                "verbose_name": "Berita",
                "verbose_name_plural": "Berita",
                "ordering": ["-tanggal_terbit"],
            },
        ),
        migrations.CreateModel(
            name="Agenda",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nama", models.CharField(max_length=250)),
                ("waktu_mulai", models.DateTimeField()),
                (
                    "keterangan_waktu",
                    models.CharField(
                        blank=True,
                        help_text="Opsional. Jika jadwal rinci belum ada, mis. 'Desember 2026 – Januari 2027'. "
                        "Teks ini ditampilkan menggantikan tanggal/jam.",
                        max_length=120,
                    ),
                ),
                ("tempat", models.CharField(blank=True, max_length=250)),
                ("keterangan", models.TextField(blank=True)),
            ],
            options={
                "verbose_name": "Agenda",
                "verbose_name_plural": "Agenda",
                "ordering": ["waktu_mulai"],
            },
        ),
        migrations.CreateModel(
            name="Dokumen",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("judul", models.CharField(max_length=200)),
                ("keterangan", models.CharField(blank=True, max_length=300)),
                ("berkas", models.FileField(upload_to="dokumen/")),
                ("tanggal_unggah", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Dokumen",
                "verbose_name_plural": "Dokumen",
                "ordering": ["-tanggal_unggah"],
            },
        ),
        migrations.CreateModel(
            name="PesanMasuk",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nama", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("subjek", models.CharField(max_length=200)),
                ("pesan", models.TextField()),
                ("waktu_kirim", models.DateTimeField(auto_now_add=True)),
                ("sudah_dibaca", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Pesan masuk",
                "verbose_name_plural": "Pesan masuk",
                "ordering": ["-waktu_kirim"],
            },
        ),
        migrations.CreateModel(
            name="TautanTerkait",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nama", models.CharField(max_length=120)),
                ("url", models.URLField()),
                ("urutan", models.PositiveIntegerField(default=0)),
            ],
            options={
                "verbose_name": "Tautan terkait",
                "verbose_name_plural": "Tautan terkait",
                "ordering": ["urutan", "id"],
            },
        ),
    ]
