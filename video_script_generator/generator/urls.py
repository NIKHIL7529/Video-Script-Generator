from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('generate-script', views.generate_script, name='generate_script'),
    path('save-script', views.save_script, name='save_script'),
    path('saved-scripts', views.get_saved_scripts, name='saved_scripts'),
    path('download-script/txt', views.download_script_txt, name='download_script_txt'),
    path('download-script/pdf', views.download_script_pdf, name='download_script_pdf'),
]