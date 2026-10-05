import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from main.forms import (
    ProjectForm,
    EducationForm,
    ExperienceForm,
    SkillGroupForm,
    LanguageForm,
)
from django.http import JsonResponse
from main.models import Experience, Education, SkillGroup, Language, Project
from django.views.decorators.http import require_POST


def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Owen Viriya Chandra",
        "npm": "2506539196",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "CS student at Universitas Indonesia, specializing in Data Science and Machine Learning"
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    title_query = request.GET.get("title", "").strip()
    
    if (not request.user.is_authenticated):
        can_edit = False
    else:
        can_edit = request.user.groups.filter(name="Editor").exists()

    context = {
            "name": "Owen Viriya Chandra",
            "title_query": title_query,
            "can_edit" : can_edit,
            "form": ExperienceForm(),
    }
    return render(request, "experience.html", context)

def show_projects(request):

    title_query = request.GET.get("title", "").strip()

    if (not request.user.is_authenticated):
        can_edit = False
    else:
        can_edit = request.user.groups.filter(name="Editor").exists()

    context = {
            "name": "Owen Viriya Chandra",
            "title_query": title_query,
            "can_edit" : can_edit,
            "form": ProjectForm(),
    }
    return render(request, "projects.html", context)


def show_skills(request):
    if (not request.user.is_authenticated):
        can_edit = False
    else:
        can_edit = request.user.groups.filter(name="Editor").exists()

    context = {
        "name": "Owen Viriya Chandra",
        "can_edit" : can_edit  ,
        "skill_group_form": SkillGroupForm(),
        "language_form": LanguageForm(),
    }
    return render(request, "skills.html", context)

@login_required(login_url="/login/")
def create_project(request):

    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New Project has been added!")
        return redirect("main:show_projects")

    context = {
        "name": "Owen Viriya Chandra",
        "form": form,
        "is_edit": False,
    }

    return render(request, "projects_form.html", context)


@login_required(login_url="/login/")
def update_project(request, project_id):
    if request.user.is_superuser or request.user.groups.filter(name="Editor").exists():
        project = get_object_or_404(Project, pk=project_id)
        form = ProjectForm(request.POST or None, instance=project)
    
        if request.method == "POST" and form.is_valid():
            form.save()
            messages.success(request, "Project has been updated!")
            return redirect("main:show_projects")
    
        context = {
            "name": "Owen Viriya Chandra",
            "form": form,
            "is_edit": True,
        }
        return render(request, "projects_form.html", context)
    raise PermissionDenied

    

@login_required(login_url="/login/")
def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New Education has been added!")
        return redirect("main:show_education")

    context = {
        "name": "Owen Viriya Chandra",
        "form": form,
        "is_edit": False,
    }

    return render(request, "education_form.html", context)


def show_education(request):
    institution_query = request.GET.get("institution", "").strip()

    if (not request.user.is_authenticated):
        can_edit = False
    else:
        can_edit = request.user.groups.filter(name="Editor").exists()

    context = {
        "name": "Owen Viriya Chandra",
        "institution_query": institution_query,
        "can_edit" : can_edit,
        "form": EducationForm(),
    }
    return render(request, "education.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "project_url": project.project_url,
                "project_image_url": project.project_image_url,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })
        

    return JsonResponse(data, safe=False)

def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.prefetch_related('starred_by').all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for experience in experiences:
        starred_users = experience.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(experience.id),
            "fields": {
                "title": experience.title,
                "description": experience.description,
                "organization": experience.organization,
                "period": experience.period,
                "logo": experience.logo,
                "location": experience.location,
                "highlights": experience.highlights,
                "tags": experience.tags,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })
        

    return JsonResponse(data, safe=False)

def get_skill_groups_json(request):
    group_query = request.GET.get("group_name", "").strip()
    skill_groups = SkillGroup.objects.all().order_by("order")

    if group_query:
        skill_groups = skill_groups.filter(group_name__icontains=group_query)

    data = []
    for skill_group in skill_groups:
        data.append({
            "pk": str(skill_group.id),
            "fields": {
                "group_name": skill_group.group_name,
                "skills": skill_group.skills,
                "order": skill_group.order,
            }
        })

    return JsonResponse(data, safe=False)

def get_languages_json(request):
    language_query = request.GET.get("language", "").strip()
    languages = Language.objects.all().order_by("order")

    if language_query:
        languages = languages.filter(language__icontains=language_query)

    data = []
    for language in languages:
        data.append({
            "pk": str(language.id),
            "fields": {
                "language": language.language,
                "proficiency": language.proficiency,
                "order": language.order,
            }
        })

    return JsonResponse(data, safe=False)

def get_education_json(request):
    institution_query = request.GET.get("institution", "").strip()
    educations = Education.objects.all()

    if institution_query:
        educations = educations.filter(institution__icontains=institution_query)

    data = []
    for education in educations:
        data.append({
            "pk": str(education.id),
            "fields": {
                "institution": education.institution,
                "period": education.period,
                "description": education.description,
                "highlight": education.highlight,
                "logo_path": education.logo_path,
            }
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project successfully deleted!")

    return redirect("main:show_projects")

@login_required(login_url="/login/")
def update_education(request, education_id):
    if request.user.is_superuser or request.user.groups.filter(name="Editor").exists():
        education = get_object_or_404(Education, pk=education_id)
        form = EducationForm(request.POST or None, instance=education)

        if request.method == "POST" and form.is_valid():
            form.save()
            messages.success(request, "Education has been updated!")
            return redirect("main:show_education")

        context = {
            "name": "Owen Viriya Chandra",
            "form": form,
            "is_edit": True,
        }

        return render(request, "education_form.html", context)
    else:
        raise PermissionDenied

@login_required(login_url="/login/")
def delete_education(request, education_id):
    if not request.user.is_superuser:
        raise PermissionDenied    
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        education.delete()
        messages.success(request, "Education successfully deleted!")

    return redirect("main:show_education")

@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New Experience has been added!")
        return redirect("main:show_experience")

    context = {
        "name": "Owen Viriya Chandra",
        "form": form,
        "is_edit": False,
    }
    return render(request, "experience_form.html", context)

@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if request.user.is_superuser or request.user.groups.filter(name="Editor").exists():
        experience = get_object_or_404(Experience, pk=experience_id)
        form = ExperienceForm(request.POST or None, instance=experience)

        if request.method == "POST" and form.is_valid():
            form.save()
            messages.success(request, "Experience has been updated!")
            return redirect("main:show_experience")

        context = {
            "name": "Owen Viriya Chandra",
            "form": form,
            "is_edit": True,
        }
        return render(request, "experience_form.html", context)
    else:
        raise PermissionDenied

@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience successfully deleted!")

    return redirect("main:show_experience")

@login_required(login_url="/login/")
def update_skill_group(request, skill_group_id):
    if request.user.is_superuser or request.user.groups.filter(name="Editor").exists():

        skill_group = get_object_or_404(SkillGroup, pk=skill_group_id)
        form = SkillGroupForm(request.POST or None, instance=skill_group)

        if request.method == "POST" and form.is_valid():
            form.save()
            messages.success(request, "Skill Group has been updated!")
            return redirect("main:show_skills")

        context = {
            "name": "Owen Viriya Chandra",
            "form": form,
            "is_edit": True,
        }
        return render(request, "skill_group_form.html", context)
    raise PermissionDenied

@login_required(login_url="/login/")
def delete_skill_group(request, skill_group_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    skill_group = get_object_or_404(SkillGroup, pk=skill_group_id)

    if request.method == "POST":
        skill_group.delete()
        messages.success(request, "Skill Group successfully deleted!")

    return redirect("main:show_skills")

@login_required(login_url="/login/")
def create_skill_group(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = SkillGroupForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New Skill Group has been added!")
        return redirect("main:show_skills")

    context = {
        "name": "Owen Viriya Chandra",
        "form": form,
        "is_edit": False,
    }
    return render(request, "skill_group_form.html", context)

@login_required(login_url="/login/")
def update_language(request, language_id):
    if request.user.is_superuser or request.user.groups.filter(name="Editor").exists():
        language = get_object_or_404(Language, pk=language_id)
        form = LanguageForm(request.POST or None, instance=language)

        if request.method == "POST" and form.is_valid():
            form.save()
            messages.success(request, "Language has been updated!")
            return redirect("main:show_skills")

        context = {
            "name": "Owen Viriya Chandra",
            "form": form,
            "is_edit": True,
        }
        return render(request, "language_form.html", context)
    else:
        raise PermissionDenied
    
@login_required(login_url="/login/")
def delete_language(request, language_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    language = get_object_or_404(Language, pk=language_id)

    if request.method == "POST":
        language.delete()
        messages.success(request, "Language successfully deleted!")

    return redirect("main:show_skills")

@login_required(login_url="/login/")
def create_language(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = LanguageForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New Language has been added!")
        return redirect("main:show_skills")

    context = {
        "name": "Owen Viriya Chandra",
        "form": form,
        "is_edit": False,
    }
    return render(request, "language_form.html", context)

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Owen Viriya Chandra",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Owen Viriya Chandra",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")


@login_required(login_url="/login/")
def toggle_experience_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")

@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Only the portfolio owner can add projects."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "The project was successfully added.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Only the portfolio owner can add experience."},
            status=403,
        )

    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "The experience was successfully added.", "pk": str(experience.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@require_POST
def create_education_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Only the portfolio owner can add education."},
            status=403,
        )

    form = EducationForm(request.POST)
    if form.is_valid():
        education = form.save()
        return JsonResponse(
            {"message": "The education entry was successfully added.", "pk": str(education.id)},
            status=201,
        )
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@require_POST
def create_skill_group_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Only the portfolio owner can add skill groups."},
            status=403,
        )

    form = SkillGroupForm(request.POST)
    if form.is_valid():
        skill_group = form.save()
        return JsonResponse(
            {"message": "The skill group was successfully added.", "pk": str(skill_group.id)},
            status=201,
        )
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@require_POST
def create_language_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Only the portfolio owner can add languages."},
            status=403,
        )

    form = LanguageForm(request.POST)
    if form.is_valid():
        language = form.save()
        return JsonResponse(
            {"message": "The language was successfully added.", "pk": str(language.id)},
            status=201,
        )
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)
