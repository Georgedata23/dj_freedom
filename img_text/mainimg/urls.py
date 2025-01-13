from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('upload_doc/<int:id_doc>/', views.upload),
    path('upload_doc/<slug:id_doc>/', views.upload_slug),

]
