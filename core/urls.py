from django.urls import path

from . import views

urlpatterns = [
    path('simular-500/', views.simular_erro_500, name='simular_erro_500'),
    path('', views.index, name='index'),
    path('api/locais/', views.api_locais, name='api_locais'),
    path('api/config-mapa/', views.api_config_mapa, name='api_config_mapa'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('admin/locais/novo/', views.admin_local_novo, name='admin_local_novo'),
    path('admin/locais/<int:pk>/editar/', views.admin_local_editar, name='admin_local_editar'),
    path('admin/locais/<int:pk>/excluir/', views.admin_local_excluir, name='admin_local_excluir'),
    path('admin/config-mapa/', views.admin_config_mapa, name='admin_config_mapa'),
]
