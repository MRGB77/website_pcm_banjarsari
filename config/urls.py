from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

admin.site.site_header = "Admin Website PCM Banjarsari"
admin.site.site_title = "Admin PCM Banjarsari"
admin.site.index_title = "Kelola isi website"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("web.urls")),
]

# Tanpa object storage, media disajikan Django sendiri (laptop dan Docker).
# Dengan object storage (USE_S3), file diambil langsung dari bucket.
if not settings.USE_S3:
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {"document_root": settings.MEDIA_ROOT},
        ),
    ]
