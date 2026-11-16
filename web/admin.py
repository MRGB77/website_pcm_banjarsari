from django.contrib import admin

from .models import (
    Agenda,
    AmalUsaha,
    Berita,
    Dokumen,
    PesanMasuk,
    Pimpinan,
    Profil,
    Ranting,
    TautanTerkait,
)


@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ("nama", "nama_singkat", "telepon", "jumlah_anggota_ktam")

    def has_add_permission(self, request):
        return not Profil.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Pimpinan)
class PimpinanAdmin(admin.ModelAdmin):
    list_display = ("nama", "jabatan", "periode", "urutan")
    list_editable = ("urutan",)
    search_fields = ("nama", "jabatan")
    list_filter = ("periode",)


@admin.register(Ranting)
class RantingAdmin(admin.ModelAdmin):
    list_display = ("nama", "ketua", "alamat", "telepon")
    search_fields = ("nama", "ketua")


@admin.register(AmalUsaha)
class AmalUsahaAdmin(admin.ModelAdmin):
    list_display = ("nama", "bidang", "alamat")
    list_filter = ("bidang",)
    search_fields = ("nama", "deskripsi")


@admin.register(Berita)
class BeritaAdmin(admin.ModelAdmin):
    list_display = ("judul", "status", "tanggal_terbit")
    list_filter = ("status",)
    search_fields = ("judul", "ringkasan", "isi")
    prepopulated_fields = {"slug": ("judul",)}
    date_hierarchy = "tanggal_terbit"


@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ("nama", "waktu_mulai", "tempat")
    search_fields = ("nama", "tempat")
    date_hierarchy = "waktu_mulai"


@admin.register(Dokumen)
class DokumenAdmin(admin.ModelAdmin):
    list_display = ("judul", "keterangan", "tanggal_unggah")
    search_fields = ("judul", "keterangan")


@admin.register(PesanMasuk)
class PesanMasukAdmin(admin.ModelAdmin):
    list_display = ("subjek", "nama", "email", "waktu_kirim", "sudah_dibaca")
    list_filter = ("sudah_dibaca",)
    search_fields = ("nama", "email", "subjek", "pesan")
    date_hierarchy = "waktu_kirim"
    # Isi pesan baca-saja; hanya penanda "sudah dibaca" yang boleh diubah.
    readonly_fields = ("nama", "email", "subjek", "pesan", "waktu_kirim")
    actions = ["tandai_dibaca"]

    def has_add_permission(self, request):
        return False

    @admin.action(description="Tandai pesan terpilih sudah dibaca")
    def tandai_dibaca(self, request, queryset):
        queryset.update(sudah_dibaca=True)


@admin.register(TautanTerkait)
class TautanTerkaitAdmin(admin.ModelAdmin):
    list_display = ("nama", "url", "urutan")
    list_editable = ("urutan",)
