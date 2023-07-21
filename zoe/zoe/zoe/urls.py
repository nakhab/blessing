from django.urls import path
from . import views

urlpatterns = [
    path('encrypt/', views.encrypt_view, name='encrypt'),
    path('download/<int:file_id>/', views.download_file, name='download'),
    path('decrypt/', views.decrypt_view, name='decrypt'),
]
