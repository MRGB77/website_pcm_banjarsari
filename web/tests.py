import tempfile
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import Agenda, AmalUsaha, Berita, PesanMasuk, Profil, Ranting


def buat_berita(judul, status=Berita.Status.TERBIT, selisih_hari=-1):
    return Berita.objects.create(
        judul=judul,
        ringkasan="Ringkasan " + judul,
        isi="Isi " + judul,
        status=status,
        tanggal_terbit=timezone.now() + timedelta(days=selisih_hari),
    )


class HalamanPublikTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Profil.objects.create(nama="PCM Uji", nama_singkat="PCM Uji", jumlah_anggota_ktam=10)
        cls.berita = buat_berita("Berita uji")

    def test_semua_halaman_publik_200(self):
        nama_url = ["beranda", "profil", "pimpinan", "ranting", "amal_usaha",
                    "berita_daftar", "agenda", "unduhan", "kontak"]
        for nama in nama_url:
            with self.subTest(halaman=nama):
                respons = self.client.get(reverse(f"web:{nama}"))
                self.assertEqual(respons.status_code, 200)

    def test_detail_berita_terbit_200(self):
        respons = self.client.get(reverse("web:berita_detail", kwargs={"slug": self.berita.slug}))
        self.assertEqual(respons.status_code, 200)
        self.assertContains(respons, "Isi Berita uji")

    def test_berita_draf_404(self):
        draf = buat_berita("Masih draf", status=Berita.Status.DRAF)
        respons = self.client.get(reverse("web:berita_detail", kwargs={"slug": draf.slug}))
        self.assertEqual(respons.status_code, 404)

    def test_berita_tanggal_masa_depan_404(self):
        nanti = buat_berita("Terbit nanti", selisih_hari=7)
        respons = self.client.get(reverse("web:berita_detail", kwargs={"slug": nanti.slug}))
        self.assertEqual(respons.status_code, 404)

    def test_berita_draf_tidak_muncul_di_daftar(self):
        buat_berita("Rahasia draf", status=Berita.Status.DRAF)
        respons = self.client.get(reverse("web:berita_daftar"))
        self.assertNotContains(respons, "Rahasia draf")

    def test_halaman_tidak_ada_404(self):
        self.assertEqual(self.client.get("/tidak-ada/").status_code, 404)


class BeritaTests(TestCase):
    def test_slug_unik_untuk_judul_sama(self):
        a = buat_berita("Judul Kembar")
        b = buat_berita("Judul Kembar")
        self.assertEqual(a.slug, "judul-kembar")
        self.assertEqual(b.slug, "judul-kembar-2")

    def test_paginasi_enam_per_halaman(self):
        for i in range(8):
            buat_berita(f"Berita nomor {i}")
        halaman1 = self.client.get(reverse("web:berita_daftar"))
        self.assertEqual(len(halaman1.context["halaman"]), 6)
        halaman2 = self.client.get(reverse("web:berita_daftar"), {"page": 2})
        self.assertEqual(len(halaman2.context["halaman"]), 2)

    def test_pencarian_berita(self):
        buat_berita("Pengajian Ahad Pagi")
        buat_berita("Rapat Pleno")
        respons = self.client.get(reverse("web:berita_daftar"), {"q": "pengajian"})
        self.assertContains(respons, "Pengajian Ahad Pagi")
        self.assertNotContains(respons, "Rapat Pleno")


class KontakTests(TestCase):
    def test_formulir_menyimpan_pesan_dan_menampilkan_sukses(self):
        respons = self.client.post(reverse("web:kontak"), {
            "nama": "Budi", "email": "budi@example.com",
            "subjek": "Tanya agenda", "pesan": "Kapan pengajian berikutnya diadakan?",
        }, follow=True)
        self.assertEqual(PesanMasuk.objects.count(), 1)
        self.assertFalse(PesanMasuk.objects.get().sudah_dibaca)
        self.assertContains(respons, "pesan Anda sudah kami terima")

    def test_pesan_terlalu_singkat_ditolak(self):
        self.client.post(reverse("web:kontak"), {
            "nama": "Budi", "email": "budi@example.com", "subjek": "Hai", "pesan": "singkat",
        })
        self.assertEqual(PesanMasuk.objects.count(), 0)


class ProfilDanAgendaTests(TestCase):
    def test_profil_hanya_boleh_satu_baris(self):
        Profil.objects.create(nama="Satu", nama_singkat="Satu")
        with self.assertRaises(ValidationError):
            Profil.objects.create(nama="Dua", nama_singkat="Dua")

    def test_agenda_dipisah_akan_datang_dan_terlaksana(self):
        Agenda.objects.create(nama="Lalu", waktu_mulai=timezone.now() - timedelta(days=3))
        Agenda.objects.create(nama="Nanti", waktu_mulai=timezone.now() + timedelta(days=3))
        self.assertEqual([a.nama for a in Agenda.objects.akan_datang()], ["Nanti"])
        self.assertEqual([a.nama for a in Agenda.objects.sudah_terlaksana()], ["Lalu"])


class AdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = get_user_model().objects.create_superuser("admin", "a@example.com", "rahasia-uji-123")

    def setUp(self):
        self.client.force_login(self.admin)

    def test_pesan_masuk_tidak_bisa_ditambah(self):
        respons = self.client.get(reverse("admin:web_pesanmasuk_add"))
        self.assertEqual(respons.status_code, 403)

    def test_profil_tidak_bisa_ditambah_jika_sudah_ada(self):
        Profil.objects.create(nama="Satu", nama_singkat="Satu")
        respons = self.client.get(reverse("admin:web_profil_add"))
        self.assertEqual(respons.status_code, 403)

    def test_profil_tidak_bisa_dihapus(self):
        profil = Profil.objects.create(nama="Satu", nama_singkat="Satu")
        respons = self.client.get(reverse("admin:web_profil_delete", args=[profil.pk]))
        self.assertEqual(respons.status_code, 403)


class SeedTests(TestCase):
    def test_seed_pcm_mengisi_data_dan_idempoten(self):
        with tempfile.TemporaryDirectory() as tmp, override_settings(MEDIA_ROOT=tmp):
            call_command("seed_pcm", verbosity=0)
            call_command("seed_pcm", verbosity=0)
        self.assertEqual(Profil.objects.count(), 1)
        self.assertEqual(Ranting.objects.count(), 7)
        self.assertGreaterEqual(AmalUsaha.objects.count(), 1)
        self.assertEqual(Berita.objects.terbit().count(), 1)
