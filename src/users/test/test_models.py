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
    fixtures = ["usergroups_fixtures.json"]

    @classmethod
    def setUpTestData(cls):
        cls.usergroup = UserGroups.objects.get(pk=1)

    def test_if_usergroup_is_an_instance(self):
        self.assertTrue(isinstance(self.usergroup, UserGroups))

    def test_usergroup_name(self):
        self.assertEqual(self.usergroup.__str__(), "one group")


class RestrictionsTest(TestCase):
    fixtures = ["restrictions_fixtures.json"]

    @classmethod
    def setUpTestData(cls):
        cls.restriction = Restrictions.objects.get(pk=1)

    def test_if_restriction_is_an_instance(self):
        self.assertTrue(isinstance(self.restriction, Restrictions))

    def test_restriction_name(self):
        self.assertEqual(self.restriction.__str__(), "Read")

    def test_restriction_code(self):
        self.assertNotEqual(self.restriction.__str__(), "RD")


class AppsTest(TestCase):
    fixtures = ["apps_fixtures.json"]

    @classmethod
    def setUpTestData(cls):
        cls.app = Apps.objects.get(pk=1)

    def test_if_app_is_an_instance(self):
        self.assertTrue(isinstance(self.app, Apps))

    def test_app_name(self):
        self.assertEqual(str(self.app), "users_app:app_list")

    def test_app_route(self):
        self.assertNotEqual(str(self.app), "user/app/list")


class RolesTest(TestCase):
    fixtures = ["roles_fixtures.json"]

    @classmethod
    def setUpTestData(cls):
        cls.role = Roles.objects.get(pk=1)

    def test_if_role_is_an_instance(self):
        self.assertTrue(isinstance(self.role, Roles))

    def test_role_name(self):
        self.assertEqual(str(self.role), "staff")


class UserProfileTest(TestCase):
    fixtures = [
        "config_fixtures.json",
        "users_fixtures.json",
        "userprofile_fixture.json",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.profile = UserProfile.objects.get(pk=1)

    def test_if_profile_is_an_instance(self):
        self.assertTrue(isinstance(self.profile, UserProfile))

    def test_profile_name(self):
        self.assertEqual(str(self.profile), self.user.username)

    def test_slug(self):
        self.assertEqual(self.profile.slug(), self.user.username)


class CurriculumVitaeTest(TestCase):
    fixtures = [
        "config_fixtures.json",
        "users_fixtures.json",
        "userprofile_fixture.json",
        "curriculumvitae_fixtures.json",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.cv = CurriculumVitae.objects.get(pk=1)

    def test_if_cv_is_an_instance(self):
        self.assertTrue(isinstance(self.cv, CurriculumVitae))

    def test_cv_name(self):
        self.assertEqual(str(self.cv), self.cv.userprofile.user.username)
