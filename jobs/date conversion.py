from datetime import datetime
from .models import Job

# Define the date format
date_format = "%b %d, %Y"  # Example: "Sep 28, 2024"

# Loop through all jobs and convert the posting_date
jobs = Job.objects.all()

for job in jobs:
    try:
        # Convert the text date to a proper date object
        posting_date = datetime.strptime(job.posting_date, date_format).date()

        # Update the new column
        job.posting_date_converted = posting_date
        job.save()

    except ValueError:
        # Handle the case where the date format is incorrect
        print(f"Skipping job with invalid posting_date: {job.posting_date}")