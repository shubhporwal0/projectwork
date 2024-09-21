import hrequests
from bs4 import BeautifulSoup
import random
import time
import sqlite3

# Connect to the Django SQLite Database
conn = sqlite3.connect('db.sqlite3', timeout=600)
table = conn.cursor()

# Create table (if it doesn't exist)
table.execute('''
    CREATE TABLE IF NOT EXISTS jobs_job (
        job_id INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT NOT NULL,
        Department TEXT NOT NULL,
        contract_location TEXT NOT NULL,
        Post_date DATE NOT NULL,
        Employment_type TEXT NOT NULL,
        application_link TEXT NOT NULL,
        long_description TEXT NOT NULL
    )
''')

# Define the base URL
base_url = 'https://jobs.sap.com/search/'

# Pagination URL parameters
params = {
    'q': '',
    'sortColumn': 'referencedate',
    'sortDirection': 'desc',
    'scrollToTable': 'true',
    'startrow': 0  # Pagination handled by `startrow`
}

# Set up headers to mimic a browser visit
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.92 Mobile Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
]

def get_random_agent():
    return random.choice(user_agents)

headers = {'User-Agent': get_random_agent()}

def scrape_jobs(page_number):
    # Adjust startrow for pagination
    params['startrow'] = page_number * 25

    # Send GET request
    response = hrequests.get(base_url, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all job listings
    jobs = soup.find_all('tr', class_='data-row')

    # Loop through each job listing
    for job in jobs:
        # Extract job title
        job_title = job.find('a', class_='jobTitle-link').text.strip()

        # Extract job location
        job_location = job.find('span', class_='jobLocation').text.strip()

        # Get job detail page URL
        job_page_link = job.find('a', {'href': True})
        full_job_page_link = 'https://jobs.sap.com{}'.format(job_page_link['href'])

        # Visit each job detail page
        job_page_response = hrequests.get(full_job_page_link, headers=headers)
        job_page_soup = BeautifulSoup(job_page_response.content, 'html.parser')

        # Extract date the job is posted
        post_date = job_page_soup.find('span', {'data-careersite-propertyid': 'date'}).text.strip()

        # Extract employment type
        employment_type = job_page_soup.find('span', {'data-careersite-propertyid': 'shifttype'}).text.strip()

        # Extract industry (department)
        department = job_page_soup.find('span', {'data-careersite-propertyid': 'department'}).text.strip()

        # Get job description
        requirements = job_page_soup.find_all('span', style="font-size:14.0px")
        requirements_bullets = []
        for span in requirements:
            for li in span.find_all_next('li'):
                requirements_bullets.append(li.get_text(strip=True))
        requirements_bullets = ' '.join(requirements_bullets)

        # Insert data into the database
        table.execute('''
            INSERT INTO jobs_job (title, contract_location, Post_date, Employment_type, 
            application_link, long_description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (job_title, job_location, post_date, employment_type,
              full_job_page_link, requirements_bullets))

        # Log the scraping (optional)
        print(f"Job Title: {job_title}, Date Posted: {post_date}")
        print(f"Employment Type: {employment_type}, Location: {job_location}, Link: {full_job_page_link}")
        print("------------------------------------------------------")

        # Commit the transaction after each page is scraped
        conn.commit()

# Start scraping with pagination
page = 17
while True:
    print(f"Scraping page {page}...")

    scrape_jobs(page)

    if page >= 20:
        print("No more jobs found or an error occurred.")
        break

    time.sleep(random.randrange(1, 10))

    page += 1

# Print completion message
print("Process completed.")

# Close the database connection when finished
conn.close()
