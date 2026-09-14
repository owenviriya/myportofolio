from django.shortcuts import render

from main.models import Experience, Education, SkillGroup, Language

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
    context = {
        "name": "Owen Viriya Chandra",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    context = {
        "name": "Owen Viriya Chandra",
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)

def show_skills(request):
    context = {
        "name": "Owen Viriya Chandra",
        "skill_groups": SkillGroup.objects.all().order_by("order"),
        "languages": Language.objects.all().order_by("order")
    }
    return render(request, "skills.html", context)