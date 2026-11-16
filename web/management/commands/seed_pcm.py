"""Mengisi database kosong dengan data riil PCM Banjarsari (tanpa gambar; foto diunggah lewat admin).

Aman dijalankan berulang kali: data dicocokkan lewat nama/judul lalu diperbarui, bukan digandakan.
Sumber setiap data dicatat di README.md (tabel "Sumber data").
Data yang tidak tersedia dikosongkan, tidak dikarang.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from django.core.management.base import BaseCommand
from django.db import transaction

from web.models import (
    Agenda,
    AmalUsaha,
    Berita,
    Pimpinan,
    Profil,
    Ranting,
    TautanTerkait,
)

WIB = ZoneInfo("Asia/Jakarta")


def waktu(tahun, bulan, hari, jam=0, menit=0):
    """Jam 00:00 berarti jam acara belum diketahui (tidak ditampilkan di website)."""
    return datetime(tahun, bulan, hari, jam, menit, tzinfo=WIB)


PROFIL = {
    "nama": "Pimpinan Cabang Muhammadiyah Banjarsari",
    "nama_singkat": "PCM Banjarsari",
    "tagline": "Memajukan Banjarsari, Mencerahkan Semesta.",
    "tentang": (
        "PCM Banjarsari adalah pimpinan Persyarikatan Muhammadiyah di tingkat kecamatan, "
        "yaitu Kecamatan Banjarsari, Kota Surakarta, Jawa Tengah. Saat ini PCM Banjarsari "
        "membawahi 7 ranting: Keprabon, Timuran, Punggawan, Ketelan, Setabelan, Kestalan, dan Gilingan.\n\n"
        "Periode Muktamar ke-48 (2022–2027) dipimpin oleh DR. Rusmanto, S.Pd.I., M.Pd.I. "
        "berdasarkan SK Pimpinan Daerah Muhammadiyah Kota Surakarta Nomor 128/KEP/III.0/D/2023.\n\n"
        "Kegiatan rutin: Kamis pertama rapat pleno cabang; Kamis kedua rapat pleno bersama majelis; "
        "Kamis ketiga pengajian pimpinan (kajian Himpunan Putusan Tarjih, dasar-dasar ibadah); "
        "Kamis keempat rapat cabang diperluas yang, bila diperlukan, melibatkan pimpinan ranting dan 'Aisyiyah. "
        "Selain itu diselenggarakan Pengajian Hari Bermuhammadiyah."
    ),
    "sejarah": (
        "PCM Banjarsari disahkan berdirinya oleh Pimpinan Muhammadiyah Wilayah Jawa Tengah melalui "
        "Surat Keputusan Nomor K/79/1978, ditetapkan di Semarang pada 24 Muharram 1398 H "
        "bertepatan dengan 4 Januari 1978 M. Dalam SK tersebut cakupan wilayah cabang meliputi 5 kelurahan.\n\n"
        "Menurut laporan Musyawarah Cabang 2023, pada saat didirikan PCM Banjarsari membawahi 5 ranting "
        "dan kini membawahi 7 ranting. SK pendirian ranting Kestalan, Timuran, Punggawan, dan Keprabon "
        "bertanggal 24 Muharram 1398 H / 4 Januari 1978 M, sedangkan ranting Gilingan 16 Shofar 1401 H / "
        "24 Desember 1980 M. Arsip SK pendirian ranting Ketelan dan Setabelan belum ditemukan di sekretariat cabang."
    ),
    "visi": "Terwujudnya masyarakat Islam yang sebenar-benarnya.",
    "misi": (
        "Menegakkan Tauhid yang murni berdasarkan Al-Quran dan As-Sunnah.\n"
        "Menyebarluaskan dan memajukan Ajaran Islam yang bersumber pada Al-Quran dan As-Sunnah "
        "yang shohihah/maqbulah.\n"
        "Mewujudkan Islam dalam kehidupan pribadi, keluarga dan masyarakat."
    ),
    "alamat_sekretariat": "Jl. KH. Ahmad Dahlan No. 35, Keprabon, Surakarta",
    "telepon": "0271-667533",
    "email": "",
    "jumlah_anggota_ktam": 513,
}

# Susunan Pimpinan PCM Banjarsari periode 2022-2027 (SK PCM No. 157/KEP/IV.0/D/2023).
PIMPINAN = [
    ("DR. Rusmanto, S.Pd.I., M.Pd.I.", "Ketua"),
    ("H.M. Dedy Purnomo, S.S., S.H., M.H.", "Wakil Ketua 1"),
    ("Sumardi", "Sekretaris"),
    ("H. Wiwit Hidayat, S.E.", "Wakil Sekretaris"),
    ("H. Farid Tribune Unique, S.E.", "Bendahara"),
    ("Fatchul Hadi, S.H.", "Wakil Bendahara"),
    ("Drs. HM. Joko Riyanto, S.H., M.M., M.H.", "Anggota"),
    ("Drs. H. Sukendar, M.Pd.", "Anggota"),
    ("Drs. H. Mahmud Hasni", "Anggota"),
    ("H.M. Rochmadin Mansyur, S.E.", "Anggota"),
    ("Andy Ratmanto, S.H.", "Anggota"),
    ("Drs. Sinwan Fajar Nahari", "Anggota"),
]

# Ketua ranting dari SK penetapan struktur masing-masing PRM. Setabelan: SK belum diterima.
RANTING = [
    ("PRM Keprabon", "H.M. Rochmadin Mansyur, S.E."),
    ("PRM Timuran", "Drs. H. Mahmud Hasni"),
    ("PRM Punggawan", "Joko Jaelani, S.Pd."),
    ("PRM Ketelan", "Drs. H. Sukendar, M.Pd."),
    ("PRM Setabelan", ""),
    ("PRM Kestalan", "H. Heru Purwoko, S.E."),
    ("PRM Gilingan", "Drs. H. Sinwan Fajar Nahari"),
]

AMAL_USAHA = [
    {
        "nama": "SMA Muhammadiyah 6 Surakarta",
        "bidang": AmalUsaha.Bidang.PENDIDIKAN,
        "alamat": "Jl. Banyuanyar, Banyuanyar, Kec. Banjarsari, Kota Surakarta, Jawa Tengah 57137",
        "deskripsi": "Sekolah menengah atas amal usaha Muhammadiyah di wilayah Banjarsari.",
    },
    {
        "nama": "Wisma Musolla Pemuda",
        "bidang": AmalUsaha.Bidang.SOSIAL,
        "alamat": "Jl. Jageran No. 10, Ketelan, Banjarsari, Surakarta",
        "deskripsi": (
            "Gedung wakaf di Jageran, Ketelan. Papan di lokasi menyebutnya tanah milik Muhammadiyah "
            "Kota Surakarta (nomor HMW 1, luas 214 m²)."
        ),
    },
    {
        "nama": "Masjid Milik Muhammadiyah (9 masjid)",
        "bidang": AmalUsaha.Bidang.SOSIAL,
        "alamat": "Ranting Gilingan, Setabelan, Kestalan, dan Keprabon",
        "deskripsi": (
            "Sembilan masjid milik Muhammadiyah yang dikelola pimpinan ranting: "
            "3 di PRM Gilingan, 2 di PRM Setabelan, 1 di PRM Kestalan, dan 3 di PRM Keprabon."
        ),
    },
]

BERITA = [
    {
        "judul": "Perkuat Sinergi, PCM, PCA, dan PCPM Banjarsari Gelar Koordinasi",
        "ringkasan": (
            "PCM, PCA, dan PCPM Banjarsari berkoordinasi di SMP Muhammadiyah 1 Simpon Surakarta "
            "membahas Pengajian Hari Bermuhammadiyah dan Pengukuhan Pengurus Masjid Al Falah Gilingan."
        ),
        "isi": (
            "Alhamdulillah, PCM, PCA, dan PCPM Banjarsari melaksanakan koordinasi pada Jumat, 16 Oktober 2026, "
            "bertempat di SMP Muhammadiyah 1 Simpon Surakarta.\n\n"
            "Pertemuan ini membahas persiapan Pengajian Hari Bermuhammadiyah dan Pengukuhan Pengurus "
            "Masjid Al Falah Gilingan.\n\n"
            "Melalui koordinasi ini, pimpinan menyatukan langkah dan menguatkan kebersamaan agar kegiatan dapat "
            "terlaksana dengan baik serta membawa manfaat bagi jamaah dan masyarakat.\n\n"
            "Semoga Allah Swt. memudahkan setiap ikhtiar dan menjadikan pengabdian ini sebagai amal jariyah. Aamiin.\n\n"
            "Bersama Menguatkan Persyarikatan, Menebar Dakwah yang Mencerahkan."
        ),
        "tanggal": waktu(2026, 10, 16, 12, 0),
    },
]

AGENDA = [
    {
        "nama": "Koordinasi PCM, PCA, dan PCPM Banjarsari",
        "waktu_mulai": waktu(2026, 10, 16),
        "keterangan_waktu": "",
        "tempat": "SMP Muhammadiyah 1 Simpon Surakarta",
        "keterangan": "Membahas Pengajian Hari Bermuhammadiyah dan Pengukuhan Pengurus Masjid Al Falah Gilingan.",
    },
    {
        "nama": "Pengajian Hari Bermuhammadiyah",
        "waktu_mulai": waktu(2026, 10, 25),
        "keterangan_waktu": "",
        "tempat": "Masjid Al Falah Gilingan",
        "keterangan": "Pengajian bermuhammadiyah bersama jamaah dan warga persyarikatan.",
    },
    {
        "nama": "Safari Dakwah",
        "waktu_mulai": waktu(2026, 12, 1),
        "keterangan_waktu": "Rencana Desember 2026 – Januari 2027 (jadwal belum pasti)",
        "tempat": "Masjid di 5 ranting",
        "keterangan": "Waktu pelaksanaan dan daftar ranting belum ditentukan.",
    },
]

TAUTAN = [
    ("PDM Kota Surakarta", "https://muhammadiyahsolo.com"),
    ("PWM Jawa Tengah", "https://pwmjateng.com"),
    ("PP Muhammadiyah", "https://muhammadiyah.or.id"),
]


class Command(BaseCommand):
    help = "Mengisi database dengan data riil PCM Banjarsari (aman dijalankan berulang)."

    @transaction.atomic
    def handle(self, *args, **options):
        profil = Profil.objects.first() or Profil()
        for kolom, nilai in PROFIL.items():
            setattr(profil, kolom, nilai)
        profil.save()

        for urutan, (nama, jabatan) in enumerate(PIMPINAN, start=1):
            Pimpinan.objects.update_or_create(
                nama=nama,
                defaults={"jabatan": jabatan, "periode": "2022–2027", "urutan": urutan},
            )

        for nama, ketua in RANTING:
            Ranting.objects.update_or_create(nama=nama, defaults={"ketua": ketua})

        for data in AMAL_USAHA:
            AmalUsaha.objects.update_or_create(
                nama=data["nama"],
                defaults={k: data[k] for k in ("bidang", "alamat", "deskripsi")},
            )

        for data in BERITA:
            Berita.objects.update_or_create(
                judul=data["judul"],
                defaults={
                    "ringkasan": data["ringkasan"],
                    "isi": data["isi"],
                    "tanggal_terbit": data["tanggal"],
                    "status": Berita.Status.TERBIT,
                },
            )

        for data in AGENDA:
            Agenda.objects.update_or_create(
                nama=data["nama"],
                defaults={k: data[k] for k in ("waktu_mulai", "keterangan_waktu", "tempat", "keterangan")},
            )

        for urutan, (nama, url) in enumerate(TAUTAN, start=1):
            TautanTerkait.objects.update_or_create(nama=nama, defaults={"url": url, "urutan": urutan})

        self.stdout.write(self.style.SUCCESS("Data PCM Banjarsari berhasil dimuat."))
