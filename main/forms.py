from django.forms import ModelForm, NumberInput, TextInput, Textarea, URLInput

from main.models import Project, Education, Experience, SkillGroup, Language


class ProjectForm(ModelForm):
    class Meta:
        model = Project

        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Project Name",
            "description": "Project Description",
            "tech_stack": "Tech Stacks",
            "project_url": "Project URL",
            "project_image_url": "Project Image URL",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Website Portofolio",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Tell something about the project",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/username/project",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...",
                }
            ),
        }


class EducationForm(ModelForm):
    class Meta:
        model = Education

        fields = [
            "institution",
            "period",
            "description",
            "highlight",
            "logo_path",
        ]

        labels = {
            "institution": "Institution Name",
            "period": "Education Period",
            "description": "Education Description",
            "highlight": "Education Highlight",
            "logo_path": "Institution Image URL",
        }

        widgets = {
            "institution": TextInput(
                attrs={
                    "placeholder": "University of XXX",
                    "maxlength": 255,
                }
            ),

            "period": TextInput(
                attrs={
                    "placeholder": "January 2023 - December 2025",
                    "maxlength": 50,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Tell something about your Education",
                    "rows": 3,
                }
            ),
            "highlight": TextInput(
                attrs={
                    "placeholder": "Education Highlight",
                }
            ),
            "logo_path": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...",
                }
            ),
        }


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience

        fields = [
            "title",
            "description",
            "organization",
            "period",
            "logo",
            "location",
            "highlights",
            "tags",
        ]

        labels = {
            "title": "Experience Title",
            "description": "Description",
            "organization": "Organization",
            "period": "Period",
            "logo": "Logo URL",
            "location": "Location",
            "highlights": "Highlights (JSON list)",
            "tags": "Tags (JSON list)",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Software Engineer",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Describe your responsibilities and work",
                    "rows": 4,
                }
            ),
            "organization": TextInput(
                attrs={
                    "placeholder": "Organization name",
                    "maxlength": 255,
                }
            ),
            "period": TextInput(
                attrs={
                    "placeholder": "January 2024 - Present",
                    "maxlength": 255,
                }
            ),
            "logo": URLInput(
                attrs={
                    "placeholder": "https://example.com/logo.png",
                }
            ),
            "location": TextInput(
                attrs={
                    "placeholder": "Jakarta, Indonesia",
                    "maxlength": 255,
                }
            ),
            "highlights": Textarea(
                attrs={
                    "placeholder": '["Led a project", "Improved a process"]',
                    "rows": 3,
                }
            ),
            "tags": Textarea(
                attrs={
                    "placeholder": '["Python", "Teamwork"]',
                    "rows": 3,
                }
            ),
        }

        help_texts = {
            "highlights": 'Enter a JSON list, for example: ["Led a project"]',
            "tags": 'Enter a JSON list, for example: ["Django", "Leadership"]',
        }


class SkillGroupForm(ModelForm):
    class Meta:
        model = SkillGroup

        fields = ["group_name", "skills", "order"]

        labels = {
            "group_name": "Skill Group Name",
            "skills": "Skills (JSON list)",
            "order": "Display Order",
        }

        widgets = {
            "group_name": TextInput(
                attrs={
                    "placeholder": "Backend Development",
                    "maxlength": 255,
                }
            ),
            "skills": Textarea(
                attrs={
                    "placeholder": '["Python", "Django"]',
                    "rows": 3,
                }
            ),
            "order": NumberInput(
                attrs={
                    "min": 0,
                    "step": 1,
                    "placeholder": "0",
                }
            ),
        }

        help_texts = {
            "skills": 'Enter a JSON list, for example: ["Python", "Django"]',
        }


class LanguageForm(ModelForm):
    class Meta:
        model = Language

        fields = ["language", "proficiency", "order"]

        labels = {
            "language": "Language",
            "proficiency": "Proficiency",
            "order": "Display Order",
        }

        widgets = {
            "language": TextInput(
                attrs={
                    "placeholder": "English",
                    "maxlength": 255,
                }
            ),
            "proficiency": TextInput(
                attrs={
                    "placeholder": "Professional working proficiency",
                    "maxlength": 255,
                }
            ),
            "order": NumberInput(
                attrs={
                    "min": 0,
                    "step": 1,
                    "placeholder": "0",
                }
            ),
        }
