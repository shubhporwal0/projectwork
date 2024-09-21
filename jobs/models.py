from django.db import models


class Job(models.Model):
    job_id = models.AutoField(primary_key=True)  # Align with the 'job_id' column as the primary key
    title = models.CharField(max_length=255, db_column='Title')  # Map to 'Title' column
    #department = models.CharField(max_length=255, db_column='Department', null=True, blank=True)  # Map to 'Department' and handle null
    contract_location = models.CharField(max_length=255, db_column='contract_location')  # Map to 'contract_location'
    posting_date = models.DateField(db_column='Post_date')  # Map to 'Post_date'
    employment_type = models.CharField(max_length=255, db_column='Employment_type')  # Map to 'Employment_type'
    application_link = models.URLField(max_length=200, db_column='application_link')  # Map to 'application_link'
    long_description = models.TextField(db_column='long_description')  # Map to 'long_description'

    # New columns added in models but missing in the database; handle nulls if needed
    career_level = models.CharField(max_length=100, null=True, blank=True)  # This column can be null
    work_mode = models.CharField(max_length=100, null=True, blank=True)  # This column can be null
    company_name = models.CharField(max_length=255, null=True, blank=True)  # This column can be null
    def __str__(self):
        return f"{self.title} at {self.company_name}"

class RecommendedJob(models.Model):
    posting_date = models.DateField()
    long_description = models.TextField()
    career_level = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    work_mode = models.CharField(max_length=100)
    contract_location = models.CharField(max_length=255)
    application_link = models.URLField(max_length=200)

    def __str__(self):
        return f"{self.title} at {self.company_name}"