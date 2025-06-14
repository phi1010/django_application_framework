from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('<str:filename>/', views.get_bundle, name='get_bundle'),
    #path('admin/', admin.site.urls),
]
