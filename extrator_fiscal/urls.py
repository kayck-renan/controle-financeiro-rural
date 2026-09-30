from django.urls import path
from . import views

app_name = "extrator_fiscal"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("api/configurar-chave/", views.configurar_chave_api, name="configurar_chave_api"),
    path("api/extrair-nf/", views.extrair_dados, name="extrair_dados"),
    path("api/exemplo/download/", views.download_exemplo, name="download_exemplo"),
    path("api/status/", views.status_api, name="status_api"),
]
