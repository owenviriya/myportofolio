from django.shortcuts import render

from main.models import Experience

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