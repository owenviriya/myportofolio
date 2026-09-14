from django.contrib import admin
from .models import Experience, Education, SkillGroup, Language


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "period", "location")

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("institution", "period")

@admin.register(SkillGroup)
class SkillGroupAdmin(admin.ModelAdmin):
    list_display = ("group_name", "order")

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("language", "proficiency", "order")