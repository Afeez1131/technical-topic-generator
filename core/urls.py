from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('process-request/', views.ajax_process_request, name='send_request'),
]
