"""API tests for the Skills page resources (SkillGroup and Language).

Both resources share the same role rules, so the scenarios live in one mixin and
each subclass only describes its model, URLs, sample data, and invalid inputs.
"""

import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Language, SkillGroup


class PortfolioResourceAPITestMixin:
    """Role, validation, star, and CSRF scenarios for one API resource."""

    model = None
    url_prefix = ""            # e.g. "skill-group" -> api:skill-group-list
    search_param = ""          # query parameter used for searching
    title_field = ""           # text field used to check that data did not change
    initial_data = {}          # data for the object created in setUp
    payload = {}               # valid full payload for POST/PUT
    invalid_inputs = []        # (changes, field_with_error) pairs
    tag_input = {}             # changes that contain HTML tags
    tag_expected = {}          # expected stored values after strip_tags

    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.editor = User.objects.create_user(username="editor", password="test-password")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.record = self.model.objects.create(**self.initial_data)
        self.list_url = reverse(f"api:{self.url_prefix}-list")
        self.detail_url = reverse(f"api:{self.url_prefix}-detail", args=[self.record.id])
        self.star_url = reverse(f"api:{self.url_prefix}-star", args=[self.record.id])

    def assert_record_unchanged(self):
        self.assertEqual(self.model.objects.count(), 1)
        self.record.refresh_from_db()
        for field, value in self.initial_data.items():
            self.assertEqual(getattr(self.record, field), value)

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.record.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("starred_by", response.data[0])
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[self.title_field], self.initial_data[self.title_field])

    def test_search_and_empty_results(self):
        keyword = self.initial_data[self.title_field][:4].upper()
        response = self.client.get(self.list_url, {self.search_param: keyword})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {self.search_param: "not-found"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_missing_record_returns_404(self):
        url = reverse(f"api:{self.url_prefix}-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            responses = [
                self.client.post(self.list_url, self.payload, format="json"),
                self.client.patch(self.detail_url, {self.title_field: "Changed"}, format="json"),
                self.client.put(self.detail_url, self.payload, format="json"),
                self.client.delete(self.detail_url),
            ]
            for response in responses:
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assert_record_unchanged()

    def test_editor_can_patch_and_put(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(
            self.detail_url, {self.title_field: "Updated by editor"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.record.refresh_from_db()
        self.assertEqual(getattr(self.record, self.title_field), "Updated by editor")
        self.assertEqual(self.record.order, self.initial_data["order"])

        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.record.refresh_from_db()
        self.assertEqual(getattr(self.record, self.title_field), self.payload[self.title_field])

    def test_editor_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assert_record_unchanged()

    def test_owner_can_create_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.model.objects.filter(pk=response.data["id"]).exists())

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(self.model.objects.filter(pk=self.record.id).exists())

    def test_put_requires_all_required_fields(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.put(self.detail_url, {"order": 5}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(self.title_field, response.data)
        self.assert_record_unchanged()

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in self.invalid_inputs:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, changes)
            self.assertIn(field, response.data)
        self.assertEqual(self.model.objects.count(), 1)

    def test_text_input_is_stripped_of_tags(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {**self.payload, **self.tag_input}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = self.model.objects.get(pk=response.data["id"])
        for field, expected in self.tag_expected.items():
            self.assertEqual(getattr(created, field), expected)

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.record.starred_by.count(), 0)

        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertTrue(self.record.starred_by.filter(pk=self.visitor.pk).exists())

        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_star_rejects_get(self):
        self.client.force_authenticate(user=self.visitor)
        response = self.client.get(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(self.model.objects.get(pk=response.data["id"]).starred_by.count(), 0)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        self.assertEqual(
            client.post(self.list_url, self.payload, format="json").status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assert_record_unchanged()

    def test_session_patch_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="editor", password="test-password"))
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.patch(
            self.detail_url, {self.title_field: "Patched with CSRF"}, format="json",
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.record.refresh_from_db()
        self.assertEqual(getattr(self.record, self.title_field), "Patched with CSRF")


class SkillGroupAPITest(PortfolioResourceAPITestMixin, APITestCase):
    model = SkillGroup
    url_prefix = "skill-group"
    search_param = "group_name"
    title_field = "group_name"
    initial_data = {"group_name": "Programming Languages", "skills": ["Python", "Java"], "order": 1}
    payload = {"group_name": "Web Development", "skills": ["Django", "HTML"], "order": 2}
    invalid_inputs = [
        ({"group_name": "   "}, "group_name"),
        ({"group_name": "<b></b>"}, "group_name"),
        ({"skills": "Python"}, "skills"),
        ({"skills": ["Python", 3]}, "skills"),
        ({"order": -1}, "order"),
        ({"order": "first"}, "order"),
    ]
    tag_input = {"group_name": "<b>Backend</b> Tools", "skills": ["<i>Docker</i>"]}
    tag_expected = {"group_name": "Backend Tools", "skills": ["Docker"]}


class LanguageAPITest(PortfolioResourceAPITestMixin, APITestCase):
    model = Language
    url_prefix = "language"
    search_param = "language"
    title_field = "language"
    initial_data = {"language": "Indonesian", "proficiency": "Native", "order": 1}
    payload = {"language": "English", "proficiency": "Professional working proficiency", "order": 2}
    invalid_inputs = [
        ({"language": "   "}, "language"),
        ({"language": "<i></i>"}, "language"),
        ({"proficiency": ""}, "proficiency"),
        ({"order": -1}, "order"),
    ]
    tag_input = {"language": "<b>Japanese</b>", "proficiency": "<script>x</script>Basic"}
    tag_expected = {"language": "Japanese", "proficiency": "xBasic"}
