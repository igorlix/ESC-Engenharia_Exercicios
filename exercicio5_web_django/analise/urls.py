from django.urls import path
from . import views

urlpatterns = [
    path('', views.analise_view, name='analise'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),
]
