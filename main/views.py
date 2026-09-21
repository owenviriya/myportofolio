from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.forms import (
    ProjectForm,
    EducationForm,
    ExperienceForm,
    SkillGroupForm,
    LanguageForm,
)
from main.models import Experience, Education, SkillGroup, Language, Project

def show_main(request):
    context = {
        "name": "Owen Viriya Chandra",
        "npm": "2506539196",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "CS student at Universitas Indonesia, specializing in Data Science and Machine Learning"
        )
    }
    return render(request, "index.html", context)


def show_experience(request):
    json_response = get_experience_json(request)
    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experience_list = [experience.object for experience in experiences]

    context = {
        "name": "Owen Viriya Chandra",
        "experience_list": experience_list,
    }
    return render(request, "experience.html", context)


def show_skills(request):
    skill_groups_response = get_skill_groups_json(request)
    skill_groups_data = serializers.deserialize(
        "json",
        skill_groups_response.content.decode("utf-8"),
    )
    skill_groups = [group.object for group in skill_groups_data]

    languages_response = get_languages_json(request)
    languages_data = serializers.deserialize(
        "json",
        languages_response.content.decode("utf-8"),
    )
    languages = [language.object for language in languages_data]

    context = {
        "name": "Owen Viriya Chandra",
        "skill_groups": skill_groups,
        "languages": languages,
    }
    return render(request, "skills.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New Project has been added!")
        return redirect("main:show_projects")

    context = {
        "name": "Owen Viriya Chandra",
        "form": form,
    }

    return render(request, "projects_form.html", context)

def create_education(request):
    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New Education has been added!")
        return redirect("main:show_education")

    context = {
        "name": "Owen Viriya Chandra",
        "form": form,
    }

    return render(request, "education_form.html", context)


def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Owen Viriya Chandra",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)

def show_education(request):
    json_response = get_education_json(request)

    educations = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    education_list = [education.object for education in educations]
    institution_query = request.GET.get("institution", "").strip()

    context = {
        "name": "Owen Viriya Chandra",
        "education_list": education_list,
        "institution_query": institution_query,
    }
    return render(request, "education.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def get_experience_json(request):
    experience_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if experience_query:
        experiences = experiences.filter(title__icontains=experience_query)

    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")

def get_skill_groups_json(request):
    group_query = request.GET.get("group_name", "").strip()
    skill_groups = SkillGroup.objects.all().order_by("order")

    if group_query:
        skill_groups = skill_groups.filter(group_name__icontains=group_query)

    skill_groups_json = serializers.serialize("json", skill_groups)
    return HttpResponse(skill_groups_json, content_type="application/json")

def get_languages_json(request):
    language_query = request.GET.get("language", "").strip()
    languages = Language.objects.all().order_by("order")

    if language_query:
        languages = languages.filter(language__icontains=language_query)

    languages_json = serializers.serialize("json", languages)
    return HttpResponse(languages_json, content_type="application/json")

def get_education_json(request):
    institution_query = request.GET.get("institution", "").strip()
    education = Education.objects.all()

    if institution_query:
        education = education.filter(institution__icontains=institution_query)

    education_json = serializers.serialize("json", education)
    return HttpResponse(education_json, content_type="application/json")


def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project successfully deleted!")

    return redirect("main:show_projects")

def update_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)
    form = EducationForm(request.POST or None, instance=education)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Education has been updated!")
        return redirect("main:show_education")

    context = {
        "name": "Owen Viriya Chandra",
        "form": form,
    }

    return render(request, "education_form.html", context)

def delete_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        education.delete()
        messages.success(request, "Education successfully deleted!")

    return redirect("main:show_education")


def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New Experience has been added!")
        return redirect("main:show_experience")

    context = {
        "name": "Owen Viriya Chandra",
        "form": form,
    }
    return render(request, "experience_form.html", context)


def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience has been updated!")
        return redirect("main:show_experience")

    context = {
        "name": "Owen Viriya Chandra",
        "form": form,
    }
    return render(request, "experience_form.html", context)


def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience successfully deleted!")

    return redirect("main:show_experience")


def update_skill_group(request, skill_group_id):
    skill_group = get_object_or_404(SkillGroup, pk=skill_group_id)
    form = SkillGroupForm(request.POST or None, instance=skill_group)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill Group has been updated!")
        return redirect("main:show_skills")

    context = {
        "name": "Owen Viriya Chandra",
        "form": form,
    }
    return render(request, "skill_group_form.html", context)


def delete_skill_group(request, skill_group_id):
    skill_group = get_object_or_404(SkillGroup, pk=skill_group_id)

    if request.method == "POST":
        skill_group.delete()
        messages.success(request, "Skill Group successfully deleted!")

    return redirect("main:show_skills")


def create_skill_group(request):
    form = SkillGroupForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New Skill Group has been added!")
        return redirect("main:show_skills")

    context = {
        "name": "Owen Viriya Chandra",
        "form": form,
    }
    return render(request, "skill_group_form.html", context)


def update_language(request, language_id):
    language = get_object_or_404(Language, pk=language_id)
    form = LanguageForm(request.POST or None, instance=language)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Language has been updated!")
        return redirect("main:show_skills")

    context = {
        "name": "Owen Viriya Chandra",
        "form": form,
    }
    return render(request, "language_form.html", context)


def delete_language(request, language_id):
    language = get_object_or_404(Language, pk=language_id)

    if request.method == "POST":
        language.delete()
        messages.success(request, "Language successfully deleted!")

    return redirect("main:show_skills")


def create_language(request):
    form = LanguageForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New Language has been added!")
        return redirect("main:show_skills")

    context = {
        "name": "Owen Viriya Chandra",
        "form": form,
    }
    return render(request, "language_form.html", context)
