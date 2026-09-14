import uuid
from django.db import models

class Experience(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    organization = models.CharField(max_length=255, blank=True, default="")
    period = models.CharField(max_length=255, blank=True, default="")
    logo = models.CharField(max_length=255, blank=True, default="") # url
    location = models.CharField(max_length=255, blank=True, default="")
    highlights = models.JSONField(default=list)
    tags = models.JSONField(default=list)

    def __str__(self):
        return self.title

class Education(models.Model):
    institution = models.CharField(max_length=255)
    period = models.CharField(max_length=50)
    description = models.TextField()
    highlight = models.CharField(max_length=255)
    logo_path = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.institution} ({self.period})"

class SkillGroup(models.Model):
    group_name = models.CharField(max_length=255)
    skills = models.JSONField(default=list)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.group_name}"

class Language(models.Model):
    language = models.CharField(max_length=255)
    proficiency = models.CharField(max_length=255)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.language}"
