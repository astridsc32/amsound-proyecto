from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('login-facial/', views.login_facial, name='login_facial'),
    #  ruta para borrar productos:
    path('eliminar-producto/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('recuperar/', views.recuperar_password, name='recuperar_password'),
path('cambiar/', views.cambiar_password, name='cambiar_password'),
path('reservar/<int:producto_id>/', views.crear_reserva, name='crear_reserva'),
path('editar/<int:id>/', views.editar_producto, name='editar_producto'),
]