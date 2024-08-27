from django.db import models

class JobListing(models.Model):
    job_title = models.CharField(max_length=200)
    job_location = models.CharField(max_length=100)
    apply_link = models.URLField(max_length=200)
    job_description = models.TextField()

    def __str__(self):
        return self.job_title

    class Meta:
        db_table = 'job_listings'  # Specify the exact table name