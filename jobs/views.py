from django.shortcuts import render

def home(request):
    return render(request, 'jobs/home.html')

def search_jobs(request):
    return render(request, 'jobs/search_results.html')
