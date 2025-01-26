from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Урлы приложения imei
    path('api/', include('imei.urls', namespace='imei')),
]
