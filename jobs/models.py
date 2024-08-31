from django.db import models

class Job(models.Model):
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