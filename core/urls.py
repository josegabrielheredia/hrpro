from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('crear-admin-seguro/', views.crear_admin_seguro, name='crear_admin_seguro'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('empleados/', views.empleado_list, name='empleado_list'),
    path('empleados/crear/', views.empleado_create, name='empleado_create'),
    path('empleados/<int:pk>/editar/', views.empleado_edit, name='empleado_edit'),
    path('empleados/<int:pk>/eliminar/', views.empleado_delete, name='empleado_delete'),
    path('empleados/<int:pk>/', views.empleado_detail, name='empleado_detail'),

    path('asistencia/', views.asistencia_list, name='asistencia_list'),
    path('asistencia/crear/', views.asistencia_create, name='asistencia_create'),
    path('asistencia/<int:pk>/editar/', views.asistencia_edit, name='asistencia_edit'),
    path('asistencia/<int:pk>/eliminar/', views.asistencia_delete, name='asistencia_delete'),

    path('nomina/', views.nomina_list, name='nomina_list'),
    path('nomina/crear/', views.nomina_create, name='nomina_create'),
    path('nomina/<int:pk>/editar/', views.nomina_edit, name='nomina_edit'),
    path('nomina/<int:pk>/eliminar/', views.nomina_delete, name='nomina_delete'),

    path('reclutamiento/', views.candidato_list, name='candidato_list'),
    path('reclutamiento/crear/', views.candidato_create, name='candidato_create'),
    path('reclutamiento/<int:pk>/editar/', views.candidato_edit, name='candidato_edit'),
    path('reclutamiento/<int:pk>/eliminar/', views.candidato_delete, name='candidato_delete'),

    path('reportes/', views.reportes, name='reportes'),
]
