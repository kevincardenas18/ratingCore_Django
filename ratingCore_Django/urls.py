"""
URL configuration for ratingCore_Django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from book_reviews import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    path('singup/', views.singup, name = 'singup'),
    path('welcome/<int:user_id>', views.welcome, name = 'welcome'),
    path('logout/', views.singout, name = 'logout'),
    path('login/', views.singin, name = 'login'),
    path('profile/<int:user_id>', views.profile, name = 'profile'),
    path('successfull', views.successfull, name = 'successfull'),
    path('profile/deleteUser/<int:user_id>', views.deleteUser),
    path('administrador/', views.administrador, name = 'administrador'),
    path('autor/', views.autor, name='autor'),
    path('libro', views.libro, name = 'libro'),
    path('libro/<int:libro_id>/', views.detalle_libro, name='detalle_libro'),
    path('libro/<int:libro_id>/guardar_valoracion/', views.guardar_valoracion, name='guardar_valoracion'),
    path('libro/<int:libro_id>/guardar_comentario/', views.guardar_comentario, name='guardar_comentario'),
    path('libro/<int:libro_id>/eliminar_comentario/', views.eliminar_comentario, name='eliminar_comentario'),
    path('autor/<int:autor_id>/', views.detalle_autor, name='detalle_autor'),
    path('categoria/', views.lista_categorias, name='lista_categorias'),
    path('categorias/agregar/', views.agregar_categoria, name='agregar_categoria'),
    path('personalizado/', views.top_personalizado, name='top_personalizado'),
    path('personalizado/calcular_compatibilidad', views.calcular_compatibilidad, name='calcular_compatibilidad'),
]

