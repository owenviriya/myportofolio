from django.test import TestCase
from django.urls import reverse

from main.models import Education, Experience, Language, SkillGroup


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Teaching Assistant of Programming Foundations 1",
            description="Membantu mahasiswa memahami dasar pemrograman.",
            organization="Faculty of Computer Science, Universitas Indonesia",
            period="Aug 2026 - Present",
            logo="/static/img/logo_fasilkom.jpg",
            location="Depok",
            highlights=[
                "Membimbing mahasiswa dalam sesi praktikum.",
                "Membantu proses debugging dan pembelajaran mandiri.",
            ],
            tags=["Teaching", "Mentoring", "Python"],
        )

        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            period="2025 - Present",
            description="Bachelor of Computer Science, Faculty of Computer Science",
            highlight="CGPA 4.00 / 4.00",
            logo_path="/static/img/logo_ui.png",
        )

        self.education_second = Education.objects.create(
            institution="SMA Atisa Dipamkara",
            period="2022 - 2025",
            description="Senior High School",
            highlight="Graduated top of the class (Best Graduate 2025)",
            logo_path="/static/img/logo_atisa.png",
        )

        self.skill_group = SkillGroup.objects.create(
            group_name="Programming Languages",
            skills=["Python", "Java", "C", "C++"],
            order=1,
        )

        self.skill_group_second = SkillGroup.objects.create(
            group_name="Machine Learning",
            skills=["PyTorch", "scikit-learn", "YOLOv8"],
            order=2,
        )

        self.language = Language.objects.create(
            language="Indonesian",
            proficiency="Native",
            order=1,
        )

        self.language_second = Language.objects.create(
            language="English",
            proficiency="Full professional proficiency, TOEIC 970 out of 990",
            order=2,
        )

    def test_main_page_is_accessible_and_has_navigation(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, "Owen Viriya Chandra")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')
        self.assertContains(response, f'href="{reverse("main:show_education")}"')
        self.assertContains(response, f'href="{reverse("main:show_skills")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), self.experience.title)
        self.assertEqual(
            self.experience.organization,
            "Faculty of Computer Science, Universitas Indonesia",
        )
        self.assertEqual(self.experience.period, "Aug 2026 - Present")
        self.assertEqual(self.experience.location, "Depok")
        self.assertEqual(
            self.experience.highlights[0],
            "Membimbing mahasiswa dalam sesi praktikum.",
        )
        self.assertEqual(self.experience.tags, ["Teaching", "Mentoring", "Python"])

    def test_experience_page_shows_dynamic_data(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, self.experience.organization)
        self.assertContains(response, self.experience.period)
        self.assertContains(response, self.experience.location)
        self.assertContains(response, self.experience.highlights[0])
        self.assertContains(response, self.experience.tags[0])
        self.assertContains(response, self.experience.logo)
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No experience have been added yet.")

    def test_education_model(self):
        self.assertEqual(str(self.education), "Universitas Indonesia (2025 - Present)")
        self.assertEqual(self.education.institution, "Universitas Indonesia")
        self.assertEqual(self.education.highlight, "CGPA 4.00 / 4.00")

    def test_education_page_shows_dynamic_data(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")
        self.assertContains(response, self.education.institution)
        self.assertContains(response, self.education.description)
        self.assertContains(response, self.education.highlight)
        self.assertContains(response, self.education.logo_path)
        self.assertContains(response, self.education_second.institution)
        self.assertContains(response, f'href="{reverse("main:show_skills")}"')

    def test_empty_education_page(self):
        Education.objects.all().delete()
        response = self.client.get(reverse("main:show_education"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No education have been added yet.")

    def test_skill_group_model(self):
        self.assertEqual(str(self.skill_group), "Programming Languages")
        self.assertEqual(self.skill_group.skills, ["Python", "Java", "C", "C++"])
        self.assertEqual(self.skill_group.order, 1)

    def test_language_model(self):
        self.assertEqual(str(self.language), "Indonesian")
        self.assertEqual(self.language.proficiency, "Native")
        self.assertEqual(self.language.order, 1)

    def test_skills_page_shows_dynamic_data_in_order(self):
        response = self.client.get(reverse("main:show_skills"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skills.html")
        self.assertContains(response, self.skill_group.group_name)
        self.assertContains(response, self.skill_group.skills[0])
        self.assertContains(response, self.skill_group_second.group_name)
        self.assertContains(response, self.language.language)
        self.assertContains(response, self.language.proficiency)
        self.assertContains(response, f'href="{reverse("main:show_education")}"')

        content = response.content.decode()
        self.assertLess(
            content.index(self.skill_group.group_name),
            content.index(self.skill_group_second.group_name),
        )
        self.assertLess(
            content.index(self.language.language),
            content.index(self.language_second.language),
        )

    def test_empty_skill_groups(self):
        SkillGroup.objects.all().delete()
        response = self.client.get(reverse("main:show_skills"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No skills have been added yet.")

    def test_empty_languages(self):
        Language.objects.all().delete()
        response = self.client.get(reverse("main:show_skills"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No languages have been added yet.")
