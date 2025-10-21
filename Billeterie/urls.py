from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from Billeterie import settings

from store.views import about, index, legal_notice

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('legal/', legal_notice, name='legal-notice'),
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('store/', include('store.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + debug_toolbar_urls()
