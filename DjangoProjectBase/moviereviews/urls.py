from django.contrib import admin
from django.urls import path, include
from movie import views as movieViews  # Si aún lo necesitas para alguna referencia

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movie.urls')),
    path('news/', include('news.urls')),
    path('recomendations/', include('recommendations.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)