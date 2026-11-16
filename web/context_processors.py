from .models import Profil, TautanTerkait


def pcm(request):
    """Profil organisasi dan tautan terkait tersedia di semua template."""
    return {
        "profil": Profil.objects.first(),
        "tautan_terkait": TautanTerkait.objects.all(),
    }
