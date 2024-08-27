import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WorkScout.settings')
django.setup()

from jobs.models import JobListing

# Define the base URL
base_url = 'https://jobs.sap.com'

# Define the search URL
search_url = 'https://jobs.sap.com/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_department=&optionsFacetsDD_customfield3=&optionsFacetsDD_country='

# Set up headers to mimic a browser visit
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

# Send a GET request to fetch the main page content
response = requests.get(search_url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Create lists to store job details
job_titles = []
job_locations = []
job_descriptions = []
apply_links = []

# Find all job listings
jobs = soup.find_all('tr', class_='data-row')

# Loop through each job listing
for job in jobs:
    # Extract job title
    job_title = job.find('a', class_='jobTitle-link').text.strip()

    # Extract job location
    job_location = job.find('span', class_='jobLocation').text.strip()

    # Get job detail page URL
    job_page_link = job.find('a', class_='jobTitle-link')['href']
    full_job_page_link = urljoin(base_url, job_page_link)

    # Visit each job detail page
    job_page_response = requests.get(full_job_page_link, headers=headers)
    job_page_soup = BeautifulSoup(job_page_response.content, 'html.parser')

    requirements = job_page_soup.find_all('span', style="font-size:14.0px")

    # Collect all bullet points under those span elements
    requirements_bullets = []
    for span in requirements:
        for li in span.find_all_next('li'):
            requirements_bullets.append(li.get_text(strip=True))

    # Find the apply button link
    apply_button = job_page_soup.find('a', class_='btn btn-primary btn-large btn-lg apply dialogApplyBtn')
    if apply_button:
        apply_link = urljoin(base_url, apply_button['href'])
    else:
        apply_link = 'Apply link not available'

    # Append to lists
    job_titles.append(job_title)
    job_locations.append(job_location)
    apply_links.append(apply_link)
    job_descriptions.append(requirements_bullets)

# Create a DataFrame
df = pd.DataFrame({
    'Job Title': job_titles,
    'Job Location': job_locations,
    'Apply Link': apply_links,
    'Job Description': job_descriptions,
})

# Loop through DataFrame and save each job listing to the database
for index, row in df.iterrows():
    JobListing.objects.create(
        job_title=row['Job Title'],
        job_location=row['Job Location'],
        apply_link=row['Apply Link'],
        job_description="; ".join(row['Job Description'])  # Join list into a single string
    )
