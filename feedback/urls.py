from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from adfs.views import sso_login, acs, saml_metadata


urlpatterns = [
    path('', include('activity.urls', namespace='activity')),
    path('metadata/', saml_metadata),
    # path('sso/login/', sso_login),
    path('acs/', acs),
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),
    path('djadmin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
