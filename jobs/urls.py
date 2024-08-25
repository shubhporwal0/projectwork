from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_jobs, name='search_jobs'),  # Add this line
]
