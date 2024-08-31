from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

'''def home(request):
    return render(request, 'jobs/job_list.html')

def search_jobs(request):
    return render(request, 'jobs/search_results.html')
from django.shortcuts import render

JOBS = {
    1: {
        'company': 'Google',
        'position': 'Senior UI/UX Designer',
        'date': '20 May, 2023',
        'salary': '$250/hr',
        'location': 'Remote',
        'tags': ['UX', 'Graphic Designer', 'Software Eng.'],
        'description': 'Are you creative, innovative and ahead of the industry standards? We want you on our leading-edge team! As our UX/UI Designer, you will...',
        'bg_color': '#cff4d2'
    },
    2: {
        'company': 'Facebook',
        'position': 'Frontend Developer',
        'date': '18 May, 2023',
        'salary': '$200/hr',
        'location': 'Remote',
        'tags': ['React', 'JavaScript', 'CSS'],
        'description': 'We are looking for a Frontend Developer who is proficient in React and has experience with building high-performance web applications...',
        'bg_color': '#ffebd7'
    },
    3: {
        'company': 'Amazon',
        'position': 'Backend Engineer',
        'date': '15 May, 2023',
        'salary': '$300/hr',
        'location': 'On-site',
        'tags': ['Python', 'Django', 'REST API'],
        'description': 'Join our team as a Backend Engineer and help us build scalable and robust backend systems using Python and Django...',
        'bg_color': '#d7efff'
    }
}

def homepage(request):
    return render(request, 'homepage.html', {'jobs': JOBS.values()})

def job_detail(request, job_id):
    job = JOBS.get(job_id)
    if job is None:
        # Handle job not found
        return render(request, '404.html', status=404)
    return render(request, 'job_detail.html', {'job': job})'''
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Job, RecommendedJob

def job_list(request):
    jobs = Job.objects.all()
    recommended_jobs = RecommendedJob.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs, 'recommended_jobs': recommended_jobs})

def job_detail_json(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        job = get_object_or_404(RecommendedJob, id=job_id)

    job_data = {
        'posting_date': job.posting_date,
        'long_description': job.long_description,
        'career_level': job.career_level,
        'title': job.title,
        'company_name': job.company_name,
        'work_mode': job.work_mode,
        'contract_location': job.contract_location,
        'application_link': job.application_link,
    }
    return JsonResponse(job_data)

def search_jobs(request):
    skill = request.GET.get('skill', '').lower()  # Get the skill from the request
    matched_jobs = Job.objects.filter(long_description__icontains=skill)  # Filter jobs containing the skill in the description

    jobs_data = []
    for job in matched_jobs:
        jobs_data.append({
            'id': job.id,
            'posting_date': job.posting_date,
            'long_description': job.long_description,
            'career_level': job.career_level,
            'title': job.title,
            'company_name': job.company_name,
            'work_mode': job.work_mode,
            'contract_location': job.contract_location,
            'application_link': job.application_link,
        })

    return JsonResponse({'jobs': jobs_data})
