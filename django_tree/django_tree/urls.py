from django.contrib import admin
from django.urls import path, include
from menu.views import MenuMain

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('', MenuMain.as_view(), name='main'),
]
