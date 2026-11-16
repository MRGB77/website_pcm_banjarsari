import re

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.text import slugify


class Profil(models.Model):
    """Profil organisasi. Hanya boleh ada satu baris."""

    nama = models.CharField(max_length=200)
    nama_singkat = models.CharField(max_length=60)
    tagline = models.CharField(max_length=200, blank=True)
    tentang = models.TextField(blank=True)
    sejarah = models.TextField(blank=True)
    visi = models.TextField(blank=True)
    misi = models.TextField(blank=True, help_text="Satu misi per baris.")
    alamat_sekretariat = models.CharField(max_length=300, blank=True)
    telepon = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    jumlah_anggota_ktam = models.PositiveIntegerField(default=0)
    gambar_hero = models.ImageField(upload_to="hero/", blank=True)

    class Meta:
        verbose_name = "Profil organisasi"
        verbose_name_plural = "Profil organisasi"

    def __str__(self):
        return self.nama

    def save(self, *args, **kwargs):
        if not self.pk and Profil.objects.exists():
            raise ValidationError("Profil organisasi hanya boleh satu baris.")
        super().save(*args, **kwargs)

    @property
    def daftar_misi(self):
        return [baris.strip() for baris in self.misi.splitlines() if baris.strip()]


class Pimpinan(models.Model):
    nama = models.CharField(max_length=200)
    jabatan = models.CharField(max_length=120)
    periode = models.CharField(max_length=20, default="2022–2027")
    foto = models.ImageField(upload_to="pimpinan/", blank=True)
    urutan = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["urutan", "id"]
        verbose_name = "Pimpinan"
        verbose_name_plural = "Pimpinan"

    def __str__(self):
        return f"{self.nama} - {self.jabatan}"

    @property
    def inisial(self):
        """Inisial dari nama tanpa gelar, dipakai saat foto belum ada."""
        kata = [k.strip(",") for k in self.nama.split()]
        kata = [k for k in kata if re.fullmatch(r"[A-Za-z']{3,}", k)
                and k.lower() not in {"alm", "prof", "drs", "dr"}]
        return "".join(k[0].upper() for k in kata[:2]) or "?"


class Ranting(models.Model):
    nama = models.CharField(max_length=120)
    ketua = models.CharField(max_length=200, blank=True)
    alamat = models.CharField(max_length=300, blank=True)
    telepon = models.CharField(max_length=40, blank=True)

    class Meta:
        ordering = ["nama"]
        verbose_name = "Ranting"
        verbose_name_plural = "Ranting"

    def __str__(self):
        return self.nama


class AmalUsaha(models.Model):
    class Bidang(models.TextChoices):
        PENDIDIKAN = "pendidikan", "Pendidikan"
        KESEHATAN = "kesehatan", "Kesehatan"
        SOSIAL = "sosial", "Sosial"
        EKONOMI = "ekonomi", "Ekonomi"

    nama = models.CharField(max_length=200)
    bidang = models.CharField(max_length=20, choices=Bidang.choices)
    deskripsi = models.TextField(blank=True)
    alamat = models.CharField(max_length=300, blank=True)
    gambar = models.ImageField(upload_to="amal-usaha/", blank=True)

    class Meta:
        ordering = ["bidang", "nama"]
        verbose_name = "Amal usaha"
        verbose_name_plural = "Amal usaha"

    def __str__(self):
        return self.nama


class BeritaQuerySet(models.QuerySet):
    def terbit(self):
        """Hanya berita berstatus terbit dan tanggalnya tidak di masa depan."""
        return self.filter(status=Berita.Status.TERBIT, tanggal_terbit__lte=timezone.now())

    def cari(self, kata):
        return self.filter(
            Q(judul__icontains=kata) | Q(ringkasan__icontains=kata) | Q(isi__icontains=kata)
        )


class Berita(models.Model):
    class Status(models.TextChoices):
        DRAF = "draf", "Draf"
        TERBIT = "terbit", "Terbit"

    judul = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    ringkasan = models.TextField(max_length=500)
    isi = models.TextField()
    gambar_sampul = models.ImageField(upload_to="berita/", blank=True)
    tanggal_terbit = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAF)

    objects = BeritaQuerySet.as_manager()

    class Meta:
        ordering = ["-tanggal_terbit"]
        verbose_name = "Berita"
        verbose_name_plural = "Berita"

    def __str__(self):
        return self.judul

    def validate_unique(self, exclude=None):
        # Keunikan slug dijamin di save(), supaya judul kembar tidak ditolak form admin.
        exclude = set(exclude or []) | {"slug"}
        super().validate_unique(exclude=exclude)

    def save(self, *args, **kwargs):
        self.slug = self._slug_unik()
        super().save(*args, **kwargs)

    def _slug_unik(self):
        dasar = (slugify(self.slug) or slugify(self.judul))[:240] or "berita"
        slug, n = dasar, 2
        while Berita.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{dasar}-{n}"
            n += 1
        return slug


class AgendaQuerySet(models.QuerySet):
    def akan_datang(self):
        return self.filter(waktu_mulai__gte=timezone.now()).order_by("waktu_mulai")

    def sudah_terlaksana(self):
        return self.filter(waktu_mulai__lt=timezone.now()).order_by("-waktu_mulai")


class Agenda(models.Model):
    nama = models.CharField(max_length=250)
    waktu_mulai = models.DateTimeField()
    keterangan_waktu = models.CharField(
        max_length=120,
        blank=True,
        help_text="Opsional. Jika jadwal rinci belum ada, mis. 'Desember 2026 – Januari 2027'. "
        "Teks ini ditampilkan menggantikan tanggal/jam.",
    )
    tempat = models.CharField(max_length=250, blank=True)
    keterangan = models.TextField(blank=True)

    objects = AgendaQuerySet.as_manager()

    class Meta:
        ordering = ["waktu_mulai"]
        verbose_name = "Agenda"
        verbose_name_plural = "Agenda"

    def __str__(self):
        return self.nama

    @property
    def punya_jam(self):
        """Jam 00:00 dianggap 'jam belum diketahui' dan tidak ditampilkan."""
        waktu = timezone.localtime(self.waktu_mulai)
        return (waktu.hour, waktu.minute) != (0, 0)


class Dokumen(models.Model):
    judul = models.CharField(max_length=200)
    keterangan = models.CharField(max_length=300, blank=True)
    berkas = models.FileField(upload_to="dokumen/")
    tanggal_unggah = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-tanggal_unggah"]
        verbose_name = "Dokumen"
        verbose_name_plural = "Dokumen"

    def __str__(self):
        return self.judul


class PesanMasuk(models.Model):
    nama = models.CharField(max_length=120)
    email = models.EmailField()
    subjek = models.CharField(max_length=200)
    pesan = models.TextField()
    waktu_kirim = models.DateTimeField(auto_now_add=True)
    sudah_dibaca = models.BooleanField(default=False)

    class Meta:
        ordering = ["-waktu_kirim"]
        verbose_name = "Pesan masuk"
        verbose_name_plural = "Pesan masuk"

    def __str__(self):
        return f"{self.subjek} - {self.nama}"


class TautanTerkait(models.Model):
    nama = models.CharField(max_length=120)
    url = models.URLField()
    urutan = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["urutan", "id"]
        verbose_name = "Tautan terkait"
        verbose_name_plural = "Tautan terkait"

    def __str__(self):
        return self.nama
