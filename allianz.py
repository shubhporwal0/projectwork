import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page to scrape
url = "https://careers.allianz.com/search/?searchby=location&createNewAlert=false&q=&locationsearch=germany"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all job listings by the repeating class
job_listings = soup.find_all('div', class_='job-tile-cell')

# Extract job details
jobs = []

for job in job_listings:
    # Extract job title
    title = job.find('a', class_='jobTitle-link').text.strip() if job.find('a', class_='jobTitle-link') else None
    # Extract job link
    link = job.find('a', class_='jobTitle-link')['href'] if job.find('a', class_='jobTitle-link') else None
    # Extract career level
    career_level = job.find('div', id=lambda x: x and x.endswith('-shifttype-value')).text.strip() if job.find('div',
                                                                                                               id=lambda
                                                                                                                   x: x and x.endswith(
                                                                                                                   '-shifttype-value')) else None

    # Append to jobs list
    jobs.append({
        'Title': title,
        'Link': f"https://careers.allianz.com{link}" if link else None,
        'Career Level': career_level
    })

# Create a DataFrame from the jobs list
df = pd.DataFrame(jobs)

# Print the DataFrame
print(df)
