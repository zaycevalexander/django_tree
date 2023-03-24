from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from user.views import LoginView, MainView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('login.html', LoginView.as_view()),
    path('', MainView.as_view(), name='main'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
