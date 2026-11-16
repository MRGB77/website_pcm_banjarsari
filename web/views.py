from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PesanForm
from .models import Agenda, AmalUsaha, Berita, Dokumen, Pimpinan, Ranting


def beranda(request):
    return render(request, "web/beranda.html", {
        "jumlah_ranting": Ranting.objects.count(),
        "jumlah_amal_usaha": AmalUsaha.objects.count(),
        "berita_terbaru": Berita.objects.terbit()[:3],
        "agenda_mendatang": Agenda.objects.akan_datang()[:3],
    })


def profil(request):
    return render(request, "web/profil.html")


def pimpinan(request):
    return render(request, "web/pimpinan.html", {"daftar_pimpinan": Pimpinan.objects.all()})


def ranting(request):
    return render(request, "web/ranting.html", {"daftar_ranting": Ranting.objects.all()})


def amal_usaha(request):
    kelompok = []
    for nilai, label in AmalUsaha.Bidang.choices:
        item = AmalUsaha.objects.filter(bidang=nilai)
        if item:
            kelompok.append((label, item))
    return render(request, "web/amal_usaha.html", {"kelompok": kelompok})


def berita_daftar(request):
    kata = request.GET.get("q", "").strip()
    queryset = Berita.objects.terbit()
    if kata:
        queryset = queryset.cari(kata)
    halaman = Paginator(queryset, 6).get_page(request.GET.get("page"))
    return render(request, "web/berita_daftar.html", {"halaman": halaman, "kata": kata})


def berita_detail(request, slug):
    berita = get_object_or_404(Berita.objects.terbit(), slug=slug)
    lainnya = Berita.objects.terbit().exclude(pk=berita.pk)[:3]
    return render(request, "web/berita_detail.html", {"berita": berita, "lainnya": lainnya})


def agenda(request):
    return render(request, "web/agenda.html", {
        "akan_datang": Agenda.objects.akan_datang(),
        "sudah_terlaksana": Agenda.objects.sudah_terlaksana(),
    })


def unduhan(request):
    return render(request, "web/unduhan.html", {"daftar_dokumen": Dokumen.objects.all()})


def kontak(request):
    if request.method == "POST":
        form = PesanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Terima kasih, pesan Anda sudah kami terima.")
            return redirect("web:kontak")
    else:
        form = PesanForm()
    return render(request, "web/kontak.html", {"form": form})
