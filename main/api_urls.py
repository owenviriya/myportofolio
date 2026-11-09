from django.urls import path

from main import api_views

app_name = "api"

urlpatterns = [
    path("experiences/", api_views.experience_list, name="experience-list"),
    path("experiences/<uuid:experience_id>/", api_views.experience_detail, name="experience-detail"),
    path("experiences/<uuid:experience_id>/star/", api_views.experience_star, name="experience-star"),
    path("projects/", api_views.project_list, name="project-list"),
    path("projects/<uuid:project_id>/", api_views.project_detail, name="project-detail"),
    path("projects/<uuid:project_id>/star/", api_views.project_star, name="project-star"),
    path("education/", api_views.education_list, name="education-list"),
    path("education/<uuid:education_id>/", api_views.education_detail, name="education-detail"),
    path("education/<uuid:education_id>/star/", api_views.education_star, name="education-star"),
    path("skill-groups/", api_views.skill_group_list, name="skill-group-list"),
    path("skill-groups/<uuid:skill_group_id>/", api_views.skill_group_detail, name="skill-group-detail"),
    path("skill-groups/<uuid:skill_group_id>/star/", api_views.skill_group_star, name="skill-group-star"),
    path("languages/", api_views.language_list, name="language-list"),
    path("languages/<uuid:language_id>/", api_views.language_detail, name="language-detail"),
    path("languages/<uuid:language_id>/star/", api_views.language_star, name="language-star"),
]
