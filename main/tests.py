from django.test import Client, TestCase
from django.urls import reverse

from main.models import Education, Experience, Language, Project, SkillGroup


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

    def test_project_create_json_and_delete_flow(self):
        response = self.client.get(reverse("main:create_project"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("main:create_project"),
            {
                "title": "Test Portfolio Project",
                "description": "A test project",
                "tech_stack": "Django, Python",
                "project_url": "https://example.com/project",
                "project_image_url": "https://example.com/project.png",
            },
        )

        self.assertRedirects(response, reverse("main:show_projects"))
        project = Project.objects.get(title="Test Portfolio Project")

        json_response = self.client.get(reverse("main:get_projects_json"))
        self.assertEqual(json_response["Content-Type"], "application/json")
        self.assertEqual(json_response.json()[0]["pk"], str(project.id))

        delete_url = reverse("main:delete_project", args=[project.id])
        response = self.client.get(delete_url)
        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertTrue(Project.objects.filter(pk=project.id).exists())

        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertFalse(Project.objects.filter(pk=project.id).exists())

    def test_projects_page_renders_shared_delete_modal(self):
        project = Project.objects.create(
            title="Modal Test Project",
            description="A project used to check the delete modal",
            tech_stack="Django",
            project_url="https://example.com/project",
            project_image_url="https://example.com/project.png",
        )

        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delete Project?")
        self.assertContains(response, "Yes, Delete")
        self.assertContains(response, f'popovertarget="delete-project-{project.id}"')

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
        self.assertContains(response, "No experience entries have been added yet.")

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
        self.assertContains(response, "No education entries have been added yet.")

    def test_education_create_update_delete_flow(self):
        create_url = reverse("main:create_education")
        response = self.client.post(
            create_url,
            {
                "institution": "Test University",
                "period": "2024 - 2026",
                "description": "Bachelor of Computer Science",
                "highlight": "Graduated with honors",
                "logo_path": "https://example.com/university.png",
            },
        )

        self.assertRedirects(response, reverse("main:show_education"))
        education = Education.objects.get(institution="Test University")

        update_url = reverse("main:update_education", args=[education.id])
        response = self.client.post(
            update_url,
            {
                "institution": "Updated University",
                "period": "2024 - 2027",
                "description": "Updated degree description",
                "highlight": "Updated highlight",
                "logo_path": "https://example.com/updated-logo.png",
            },
        )

        self.assertRedirects(response, reverse("main:show_education"))
        education.refresh_from_db()
        self.assertEqual(education.institution, "Updated University")

        delete_url = reverse("main:delete_education", args=[education.id])
        response = self.client.get(delete_url)
        self.assertRedirects(response, reverse("main:show_education"))
        self.assertTrue(Education.objects.filter(pk=education.id).exists())

        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse("main:show_education"))
        self.assertFalse(Education.objects.filter(pk=education.id).exists())

    def test_education_create_form_requires_csrf_token(self):
        csrf_client = Client(enforce_csrf_checks=True)
        create_url = reverse("main:create_education")
        response = csrf_client.get(create_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="csrfmiddlewaretoken"')

        response = csrf_client.post(
            create_url,
            {
                "institution": "Test University",
                "period": "2024 - 2026",
                "description": "Bachelor of Computer Science",
                "highlight": "Graduated with honors",
                "logo_path": "https://example.com/university.png",
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_education_json_endpoint_returns_serialized_data(self):
        response = self.client.get(reverse("main:get_education_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(
            response.json()[0]["fields"]["institution"],
            self.education.institution,
        )

    def test_experience_create_update_delete_flow(self):
        create_url = reverse("main:create_experience")
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            create_url,
            {
                "title": "Test Experience",
                "description": "A test experience",
                "organization": "Test Organization",
                "period": "2024 - Present",
                "logo": "https://example.com/logo.png",
                "location": "Depok",
                "highlights": '["Led a project"]',
                "tags": '["Python"]',
            },
        )

        self.assertRedirects(response, reverse("main:show_experience"))
        experience = Experience.objects.get(title="Test Experience")

        response = self.client.get(reverse("main:update_experience", args=[experience.id]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("main:update_experience", args=[experience.id]),
            {
                "title": "Updated Experience",
                "description": "Updated description",
                "organization": "Updated Organization",
                "period": "2025 - Present",
                "logo": "https://example.com/updated-logo.png",
                "location": "Jakarta",
                "highlights": '["Improved a process"]',
                "tags": '["Django"]',
            },
        )

        self.assertRedirects(response, reverse("main:show_experience"))
        experience.refresh_from_db()
        self.assertEqual(experience.title, "Updated Experience")
        self.assertEqual(experience.highlights, ["Improved a process"])

        delete_url = reverse("main:delete_experience", args=[experience.id])
        self.client.post(delete_url)
        self.assertFalse(Experience.objects.filter(pk=experience.id).exists())

    def test_skill_group_and_language_create_update_delete_flows(self):
        response = self.client.get(reverse("main:create_skill_group"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("main:create_skill_group"),
            {
                "group_name": "Test Skills",
                "skills": '["Python", "Django"]',
                "order": 3,
            },
        )
        self.assertRedirects(response, reverse("main:show_skills"))
        skill_group = SkillGroup.objects.get(group_name="Test Skills")

        response = self.client.get(
            reverse("main:update_skill_group", args=[skill_group.id])
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("main:update_skill_group", args=[skill_group.id]),
            {
                "group_name": "Updated Skills",
                "skills": '["HTML", "CSS"]',
                "order": 4,
            },
        )
        self.assertRedirects(response, reverse("main:show_skills"))
        skill_group.refresh_from_db()
        self.assertEqual(skill_group.skills, ["HTML", "CSS"])

        self.client.post(reverse("main:delete_skill_group", args=[skill_group.id]))
        self.assertFalse(SkillGroup.objects.filter(pk=skill_group.id).exists())

        response = self.client.get(reverse("main:create_language"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("main:create_language"),
            {
                "language": "French",
                "proficiency": "Intermediate",
                "order": 3,
            },
        )
        self.assertRedirects(response, reverse("main:show_skills"))
        language = Language.objects.get(language="French")

        response = self.client.get(reverse("main:update_language", args=[language.id]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("main:update_language", args=[language.id]),
            {
                "language": "Spanish",
                "proficiency": "Advanced",
                "order": 4,
            },
        )
        self.assertRedirects(response, reverse("main:show_skills"))
        language.refresh_from_db()
        self.assertEqual(language.language, "Spanish")

        self.client.post(reverse("main:delete_language", args=[language.id]))
        self.assertFalse(Language.objects.filter(pk=language.id).exists())

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
