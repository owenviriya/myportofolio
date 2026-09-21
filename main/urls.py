from django.urls import path

from main.views import (show_main, show_experience, show_education, 
                        show_skills, create_project, show_projects, get_projects_json,
                        delete_project, create_education, update_education, delete_education,
                        get_education_json, get_experience_json,
                        get_skill_groups_json, get_languages_json,
                        update_experience, delete_experience,
                        update_skill_group, delete_skill_group,
                        update_language, delete_language,
                        create_experience, create_skill_group, create_language,
                        )

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/<uuid:experience_id>/edit/", update_experience, name="update_experience"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("education/", show_education, name="show_education"),
    path("skills/", show_skills, name="show_skills"),
    path("skills/groups/add/", create_skill_group, name="create_skill_group"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/", show_projects, name="show_projects"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/",delete_project,name="delete_project"),
    path("api/experience/", get_experience_json, name="get_experience_json"),
    path("api/skill-groups/", get_skill_groups_json, name="get_skill_groups_json"),
    path("api/languages/", get_languages_json, name="get_languages_json"),
    path("skills/groups/<uuid:skill_group_id>/edit/", update_skill_group, name="update_skill_group"),
    path("skills/groups/<uuid:skill_group_id>/delete/", delete_skill_group, name="delete_skill_group"),
    path("skills/languages/<uuid:language_id>/edit/", update_language, name="update_language"),
    path("skills/languages/<uuid:language_id>/delete/", delete_language, name="delete_language"),
    path("skills/languages/add/", create_language, name="create_language"),
    path("education/add/", create_education, name="create_education"),
    path("education/<uuid:education_id>/edit/", update_education, name="update_education"),
    path("education/<uuid:education_id>/delete/", delete_education, name="delete_education"),
    path("api/education/", get_education_json, name="get_education_json"),
]
