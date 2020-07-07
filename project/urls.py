from core.sitemaps import PostSitemap
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from dj_rest_auth.registration.views import VerifyEmailView
from django.conf.urls.i18n import i18n_patterns
from .views import UserDetailView

sitemaps = {
    'blogs': PostSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns += i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('', include('core.urls')),
    path('', include('contacts.urls')),
    path('', include('blogs.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('pwa.urls')),
    path('profiles/', include('profiles.urls')),
    path('perfomance/', include('products.urls')),
    path('upload/', include('csvs.urls')),
    path('customers/', include('customers.urls')),

    # Restframework urls
    path('accounts/', include('allauth.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/registration/account-confirm-email/', VerifyEmailView.as_view(),
         name='account_email_verification_sent'),
    path("api/blog/", include('blogs.api.urls')),
    path("me/", UserDetailView.as_view(), name="me"),

    prefix_default_language=False
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
