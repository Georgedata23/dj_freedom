from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('upload_doc/<int:id_doc>/', views.upload, name='upload'),
    path('upload_doc/<slug:id_doc_slug>/', views.upload_slug, name='pydantic is cool!'),
    path('analyse/', views.analyse, name='analyse'),
    path('login/', auth_views.LoginView.as_view(template_name='mainimg/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login'), name='logout'),
    path('delete/', views.DeleteFormView.as_view(), name='delete')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
