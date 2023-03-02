# django modules
from django.urls import reverse, reverse_lazy, resolve
from django.http import HttpResponse
from django.core.validators import validate_slug

from django.test import TestCase
from users.models import (
    UserGroups,
    Restrictions,
    Apps,
    Roles,
    Rules,
    UserProfile,
    CurriculumVitae,
)
from django.contrib.auth.models import User
from config.models import Cities, Countries, Districts, Cities, DocumentType

from datetime import datetime


# Create your tests here.
class UserGroupTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usergroup = UserGroups.objects.create(
            group_name="one group",
            description="one group description",
            created_at=datetime.now(),
        )

    def test_if_usergroup_is_an_instance(self):
        self.assertTrue(isinstance(self.usergroup, UserGroups))

    def test_usergroup_name(self):
        self.assertEqual(self.usergroup.__str__(), "one group")


class RestrictionsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.restriction = Restrictions.objects.create(
            code="RD",
            name="Read",
            description="Don't read",
            created_at=datetime.now(),
        )

    def test_if_restriction_is_an_instance(self):
        self.assertTrue(isinstance(self.restriction, Restrictions))

    def test_restriction_name(self):
        self.assertEqual(self.restriction.__str__(), "Read")

    def test_restriction_code(self):
        self.assertNotEqual(self.restriction.__str__(), "RD")


class AppsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.app = Apps.objects.create(
            name="users_app:app_list",
            route="user/app/list",
            description="application list",
            created_at=datetime.now(),
        )

    def test_if_app_is_an_instance(self):
        self.assertTrue(isinstance(self.app, Apps))

    def test_app_name(self):
        self.assertEqual(str(self.app), "users_app:app_list")

    def test_app_route(self):
        self.assertNotEqual(str(self.app), "user/app/list")


class RolesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.role = Roles.objects.create(
            role_name="staff",
            description="administrative actors",
            created_at=datetime.now(),
        )

    def test_if_role_is_an_instance(self):
        self.assertTrue(isinstance(self.role, Roles))

    def test_role_name(self):
        self.assertEqual(str(self.role), "staff")


class UserProfileTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="admin", password="123")
        country = Countries.objects.create(
            iso="COL",
            name="Colombia",
            created_at=datetime.now(),
        )
        district = Districts.objects.create(
            iso="SAN",
            zipcode="68XXXX",
            name="Santander",
            country=country,
            created_at=datetime.now(),
        )
        city = Cities.objects.create(
            zipcode="680001",
            name="Bucaramanga",
            district=district,
            created_at=datetime.now(),
        )
        document_type = DocumentType.objects.create(
            acronym="CC", name="Cédula de ciudadanía"
        )
        document_type.country.set([country])
        cls.profile = UserProfile.objects.create(
            user=cls.user,
            document_type=document_type,
            id_number="1001222333",
            phone="3001112222",
            email="admin@example.com",
            city=city,
            created_at=datetime.now(),
        )

    def test_if_profile_is_an_instance(self):
        self.assertTrue(isinstance(self.profile, UserProfile))

    def test_profile_name(self):
        self.assertEqual(str(self.profile), self.user.username)

    def test_slug(self):
        self.assertEqual(self.profile.slug(), self.user.username)


class CurriculumVitaeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="admin", password="123")
        country = Countries.objects.create(
            iso="COL",
            name="Colombia",
            created_at=datetime.now(),
        )
        district = Districts.objects.create(
            iso="SAN",
            zipcode="68XXXX",
            name="Santander",
            country=country,
            created_at=datetime.now(),
        )
        city = Cities.objects.create(
            zipcode="680001",
            name="Bucaramanga",
            district=district,
            created_at=datetime.now(),
        )
        document_type = DocumentType.objects.create(
            acronym="CC", name="Cédula de ciudadanía"
        )
        document_type.country.set([country])
        profile = UserProfile.objects.create(
            user=cls.user,
            document_type=document_type,
            id_number="1001222333",
            phone="3001112222",
            email="admin@example.com",
            city=city,
            created_at=datetime.now(),
        )
        cls.cv = CurriculumVitae.objects.create(
            userprofile=profile,
            cv_path="/cv.png",
        )

    def test_if_cv_is_an_instance(self):
        self.assertTrue(isinstance(self.cv, CurriculumVitae))

    def test_cv_name(self):
        self.assertEqual(str(self.cv), self.cv.userprofile.user.username)
