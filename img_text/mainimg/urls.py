from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('upload_doc/<int:id_doc>/', views.upload, name='upload'),
    path('upload_doc/<slug:id_doc_slug>/', views.upload_slug, name='pydantic is cool!'),
    path('analyse/<int:id_doc>/', views.analyse, name='analyse'),
]
