from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),  # Homepage
    path('search/', views.search_jobs, name='search_jobs'),  # Search functionality
    #path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('job-details/<int:job_id>/', views.job_detail_json, name='job_detail_json'),  # Add this line
    path('interview-tips/', views.interview_tips, name='interview_tips'),  # new path for interview tips
]
