from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('', include('members.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]

# Serving media files in development mode 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
