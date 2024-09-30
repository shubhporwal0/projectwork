import hrequests  # Use requests if hrequests isn't correct
from bs4 import BeautifulSoup
import sqlite3
import random

# Define user agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    # Add more user agents if needed
]

def get_random_agent():
    return random.choice(user_agents)

# Function to scrape the first page of SAP jobs and update the database
def scraperefresh_jobs():
    base_url = 'https://jobs.sap.com/search/'
    params = {
        'q': '',
        'sortColumn': 'referencedate',
        'sortDirection': 'desc',
        'scrollToTable': 'true',
        'startrow': 0  # Page 1 (first 25 jobs)
    }

    headers = {'User-Agent': get_random_agent()}
    response = hrequests.get(base_url, params=params, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    jobs = soup.find_all('tr', class_='data-row')

    # Connect to the Django SQLite Database
    conn = sqlite3.connect('db.sqlite3', timeout=600)
    table = conn.cursor()

    for job in jobs:
        # Extract job details
        job_title = job.find('a', class_='jobTitle-link').text.strip()
        job_location = job.find('span', class_='jobLocation').text.strip()
        job_page_link = job.find('a', {'href': True})['href']
        full_job_page_link = f"https://jobs.sap.com{job_page_link}"

        # Check if job with this application link already exists
        table.execute('SELECT * FROM jobs_job WHERE application_link = ?', (full_job_page_link,))
        if table.fetchone() is not None:
            print(f"Job already exists: {job_title}")
            continue

        # Scrape additional details from the job page
        job_page_response = hrequests.get(full_job_page_link, headers=headers)
        job_page_soup = BeautifulSoup(job_page_response.content, 'html.parser')
        post_date = job_page_soup.find('span', {'data-careersite-propertyid': 'date'}).text.strip()
        employment_type = job_page_soup.find('span', {'data-careersite-propertyid': 'shifttype'}).text.strip()
        department = job_page_soup.find('span', {'data-careersite-propertyid': 'department'}).text.strip()
        long_description = " ".join(
            [li.get_text(strip=True) for li in job_page_soup.find_all('span', style="font-size:14.0px")]
        )

        # Insert new job into the database
        table.execute('''
            INSERT INTO jobs_job (Title, contract_location, posting_date, Employment_type, 
            application_link, long_description, company_name)
            VALUES (?, ?, ?, ?, ?, ?, "SAP")
        ''', (job_title, job_location, post_date, employment_type, full_job_page_link, long_description))

        print(f"Added new job: {job_title}")

    conn.commit()
    conn.close()

    print("Page 1 scraping and database update completed.")
