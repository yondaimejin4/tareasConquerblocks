from django.db import models


class Service(models.Model):
    title = models.CharField(max_length=120)
    short_description = models.CharField(max_length=200)
    details = models.TextField()
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ContactLead(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    company = models.CharField(max_length=120, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
