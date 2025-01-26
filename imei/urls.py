from django.urls import path

from imei.apps import ImeiConfig
from imei.views import TokenTGPostView

app_name = ImeiConfig.name

urlpatterns = [
    # Урл для передачи токена
    path('check_imei/', TokenTGPostView.as_view(), name='your-post-view'),
]