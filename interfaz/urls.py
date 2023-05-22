from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("simulacion", views.simulacion, name="simulacion"),
    path("resultados", views.resultados, name="resultados"),
    path("sobre_el_proyecto", views.sobre_el_proyecto, name="sobre_el_proyecto"),
    path("contacto", views.contacto, name="contacto")
]
