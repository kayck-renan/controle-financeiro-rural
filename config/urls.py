"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from extrator_fiscal import views as extrator_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', extrator_views.login_view, name='login_root'),
    path('logout/', extrator_views.logout_view, name='logout_root'),
    path('', include('extrator_fiscal.urls')),
]
