from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.recipes.views import recipe_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.recipes.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('s/<int:recipe_id>/', recipe_redirect, name='recipe_short_url'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 