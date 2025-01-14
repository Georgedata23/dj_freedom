from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('upload_doc/<int:id_doc>/', views.upload, name='upload'),
    path('upload_doc/<slug:id_doc_slug>/', views.upload_slug, name='pydantic is cool!'),
    path('analyse/<int:id_doc>/', views.analyse, name='analyse'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('protected/', views.ProtectedPageView.as_view(), name='protected'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login'), name='logout'),

]
