from core.sitemaps import PostSitemap
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns


sitemaps = {
    'blogs': PostSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns += i18n_patterns (
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('', include('core.urls')),
    path('', include('contacts.urls')),
    path('', include('blogs.urls')),
    path('accounts/', include('allauth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('pwa.urls')),
    path('profiles/', include('profiles.urls')),
    prefix_default_language=False
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
