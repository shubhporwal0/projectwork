from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Job, RecommendedJob

def job_list(request):
    jobs = Job.objects.all()
    recommended_jobs = RecommendedJob.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs, 'recommended_jobs': recommended_jobs})

def job_detail_json(request, job_id):
    # Updated to use job_id instead of id, for both Job and RecommendedJob models
    try:
        job = Job.objects.get(job_id=job_id)
    except Job.DoesNotExist:
        job = get_object_or_404(RecommendedJob, job_id=job_id)  # Also checking RecommendedJob for job_id

    # Prepare job data to return as JSON
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
            'job_id': job.job_id,  # Use job_id instead of id
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

def interview_tips(request):
    # New view for Interview Tips
    return render(request, 'jobs/interview_tips.html')

def about_us(request):
    return render(request, 'jobs/about_us.html')
