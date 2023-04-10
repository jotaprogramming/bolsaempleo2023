# python modules
from pprint import pprint

# django modules
from django.urls import reverse, reverse_lazy, resolve
from django.http import HttpResponse
from django.core.validators import validate_slug
from django.test import RequestFactory
from django.test import TestCase
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import path

from users.models import (
    UserGroups,
    Restrictions,
    Apps,
    UserRules,
    UserRules,
    UserProfile,
    CurriculumVitae,
)
from users.views import (
    UserGroupList,
    UserGroupCreate,
    UserGroupEditModal,
    UserGroupDeleteModal,
    RestrictionList,
    RestrictionCreate,
    RestrictionEditModal,
    RestrictionDeleteModal,
    AppList,
    AppEditModal,
    RoleList,
    RoleCreate,
    RoleEditModal,
    RoleDeleteModal,
    UserRulesList,
    UserRulesCreate,
    UserRulesEditModal,
    UserRulesDeleteModal,
    UserList,
    UserCreate,
    UserEditModal,
    UserDeleteModal,
    UserLogin,
    UserLogout,
    # RegisterView,
    UserProfileDetail,
    UserProfileCreate,
    UserProfileEdit,
    PreRegisterView,
    RegisterStudentView,
    RegisterCompanyView,
    CredentialsRecoverView,
)
from users.urls import urlpatterns as url_users
from config.models import Cities, Countries, Districts, Cities, DocumentType

from datetime import datetime


# Create your tests here.


class UserGroupViewsTest(TestCase):
    fixtures = ["users_fixtures.json", "usergroups_fixtures.json"]
    objview = UserGroupList()
    path = reverse("users_app:usergroup_list")

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.factory = RequestFactory()
        request = cls.factory.get(cls.path)
        request.user = cls.user
        cls.view = cls.objview
        cls.view.request = request

        cls.redirect = reverse("users_app:usergroup_list")

    def test_get_context_data(self):
        kwargs = {}
        response = UserGroupList.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)


class UserGroupListTest(UserGroupViewsTest):
    def test_get_queryset(self):
        queryset = self.view.get_queryset()
        data = UserGroups.objects.all().order_by("id")

        self.assertQuerysetEqual(queryset, data)


class UserGroupFormTest(UserGroupViewsTest):
    fixtures = ["users_fixtures.json", "usergroups_fixtures.json"]
    objview = UserGroupCreate()
    path = reverse("users_app:usergroup_add")

    def test_successfull(self):
        post = {
            "group_name": "three group",
            "description": "three group description",
        }
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, post)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)

    def test_user_groups_duplicates(self):
        post = {
            "group_name": "two group",
            "description": "two group description",
        }
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, post)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)


class UserGroupCreateTest(UserGroupFormTest):
    def test_user_groups_exception(self):
        post = {
            "group_name": "",
            "description": "number group description",
        }
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, post)

        self.assertEqual(response.status_code, 200)


class UserGroupEditModalTest(UserGroupCreateTest):
    objview = UserGroupEditModal()
    path = reverse("users_app:usergroup_edit", args=[1])

    def test_get_context_data(self):
        kwargs = {"pk": 1}
        response = UserGroupEditModal.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)


class UserGroupDeleteModalTest(UserGroupCreateTest):
    fixtures = ["users_fixtures.json", "usergroups_fixtures.json"]
    objview = UserGroupDeleteModal()
    path = reverse("users_app:usergroup_delete", args=[1])

    def test_get_context_data(self):
        kwargs = {"pk": 1}
        response = UserGroupDeleteModal.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)

    def test_successfull(self):
        post = {}
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, post)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)

    def test_user_groups_duplicates(self):
        post = {}
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, post)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)

    def test_user_groups_exception(self):
        post = {}
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, post)

        self.assertEqual(response.status_code, 302)


class RestrictionViewsTest(TestCase):
    fixtures = ["users_fixtures.json", "restrictions_fixtures.json"]
    objview = RestrictionList()
    path = reverse("users_app:restriction_list")

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.factory = RequestFactory()
        request = cls.factory.get(cls.path)
        request.user = cls.user
        cls.view = cls.objview
        cls.view.request = request

        cls.redirect = reverse("users_app:restriction_list")

    def test_get_context_data(self):
        kwargs = {}
        response = RestrictionList.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)


class RestrictionListTest(RestrictionViewsTest):
    def test_get_queryset(self):
        queryset = self.view.get_queryset()
        data = Restrictions.objects.all().order_by("id")

        self.assertQuerysetEqual(queryset, data)


class RestrictionCreateTest(RestrictionViewsTest):
    fixtures = ["users_fixtures.json", "restrictions_fixtures.json"]
    objview = RestrictionCreate()
    path = reverse("users_app:restriction_add")

    def test_successfull(self):
        post = {
            "code": "DEL",
            "name": "Delete",
            "description": "delete description",
        }
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, post)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)

    def test_get_context_data(self):
        kwargs = {}
        response = RestrictionCreate.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)

    def test_restriction_exception(self):
        post = {
            "code": "",
            "name": "",
            "description": "edit description",
        }
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, post)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)

    def test_restriction_duplicates(self):
        post = {
            "code": "RD",
            "name": "Read",
            "description": "Don't read",
        }
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, post)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)


class RestrictionEditModalTest(RestrictionCreateTest):
    objview = RestrictionEditModal()
    path = reverse("users_app:restriction_edit", args=[1])

    def test_get_context_data(self):
        kwargs = {"pk": 1}
        response = RestrictionEditModal.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)

    def test_restriction_duplicates(self):
        post = {
            "code": "RD",
            "name": "Read",
            "description": "Don't read",
        }
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, post)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)


class RestrictionDeleteModalTest(RestrictionViewsTest):
    fixtures = ["users_fixtures.json", "restrictions_fixtures.json"]
    objview = RestrictionDeleteModal()
    path = reverse("users_app:restriction_delete", args=[1])

    def test_get_context_data(self):
        kwargs = {"pk": 1}
        response = RestrictionDeleteModal.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)

    def test_successfull(self):
        post = {}
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, post)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)

    def test_restriction_exception(self):
        post = {}
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, post)

        self.assertEqual(response.status_code, 302)


class AppViewsTest(TestCase):
    fixtures = ["users_fixtures.json", "apps_fixtures.json"]
    objview = AppList()
    path = reverse("users_app:app_list")

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.factory = RequestFactory()
        request = cls.factory.get(cls.path)
        request.user = cls.user
        cls.view = cls.objview
        cls.view.request = request

        cls.redirect = reverse("users_app:app_list")


class AppListTest(AppViewsTest):
    def test_get_queryset(self):
        queryset = self.view.get_queryset()
        data = Apps.objects.all().order_by("id")

        self.assertQuerysetEqual(queryset, data)

    def test_get_context_data(self):
        kwargs = {}
        url_users.append(
            path(
                "test/app/list",
                AppList.as_view(),
                name="app_list",
            ),
        )
        response = AppList.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)


class AppEditModalTest(AppListTest):
    objview = AppEditModal()
    path = reverse("users_app:app_edit", args=[1])

    def test_successfull(self):
        post = post = {
            "name": "test_app_list",
            "route": "test/app/list",
            "description": "App",
        }
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, post)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)

    def test_get_context_data(self):
        kwargs = {"pk": 1}
        response = AppEditModal.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)


class RoleViewsTest(TestCase):
    fixtures = ["users_fixtures.json", "roles_fixtures.json"]
    objview = RoleList()
    path = reverse("users_app:role_list")

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.factory = RequestFactory()
        request = cls.factory.get(cls.path)
        request.user = cls.user
        cls.view = cls.objview
        cls.view.request = request

        cls.redirect = reverse("users_app:role_list")

    def test_get_context_data(self):
        kwargs = {}
        response = RoleList.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)


class RoleListTest(RoleViewsTest):
    def test_get_queryset(self):
        queryset = self.view.get_queryset()
        data = UserRules.objects.all().order_by("id")

        self.assertQuerysetEqual(queryset, data)


class RoleCreateTest(RoleViewsTest):
    fixtures = ["users_fixtures.json", "roles_fixtures.json"]
    objview = RoleCreate()
    path = reverse("users_app:role_add")

    def test_successfull(self):
        post = {
            "role_name": "admin",
            "description": "admin description",
        }
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, post)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)

    def test_get_context_data(self):
        kwargs = {}
        response = RoleCreate.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)

    def test_role_exception(self):
        post = {
            "role_name": "",
            "description": "role description",
        }
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, post)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)

    def test_role_duplicates(self):
        post = {
            "role_name": "staff",
            "description": "staff description",
        }
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, post)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)


class RoleEditModalTest(RoleCreateTest):
    objview = RoleEditModal()
    path = reverse("users_app:role_edit", args=[1])

    def test_get_context_data(self):
        kwargs = {"pk": 1}
        response = RoleEditModal.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)

    def test_role_duplicates(self):
        post = {
            "role_name": "staff",
            "description": "staff description",
        }
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, post)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)


class RoleDeleteModalTest(RoleViewsTest):
    fixtures = ["users_fixtures.json", "roles_fixtures.json"]
    objview = RoleDeleteModal()
    path = reverse("users_app:role_delete", args=[1])

    def test_get_context_data(self):
        kwargs = {"pk": 1}
        response = RoleDeleteModal.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)

    def test_successfull(self):
        post = {}
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, post)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)

    def test_role_exception(self):
        post = {}
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, post)

        self.assertEqual(response.status_code, 302)


class UserRulesViewsTest(TestCase):
    fixtures = [
        "users_fixtures.json",
        "apps_fixtures.json",
        "restrictions_fixtures.json",
        "roles_fixtures.json",
        "rules_fixtures.json",
    ]
    objview = UserRulesList()
    path = reverse("users_app:user_list")
    post_success = {
        "user": 1,
        "app": [1],
        "restriction": [1],
        "role": [1],
    }
    post_exception = {
        "user": 0,
        "app": [1],
        "restriction": [1],
        "role": [1],
    }

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.factory = RequestFactory()
        request = cls.factory.get(cls.path)
        request.user = cls.user
        cls.view = cls.objview
        cls.view.request = request

        cls.redirect = reverse("users_app:rule_list")

    def test_get_context_data(self):
        kwargs = {}
        response = UserRulesList.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)


class UserRulesListTest(UserRulesViewsTest):
    def test_get_queryset(self):
        queryset = self.view.get_queryset()
        data = UserRules.objects.all().order_by("id")

        self.assertQuerysetEqual(queryset, data)


class UserRulesCreateTest(UserRulesViewsTest):
    objview = UserRulesCreate()
    path = reverse("users_app:rule_add")

    def test_successfull(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, self.post_success)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)

    def test_get_context_data(self):
        kwargs = {}
        response = UserRulesCreate.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)

    def test_rule_exception(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, self.post_exception)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)


class UserRulesEditModalTest(UserRulesCreateTest):
    objview = UserRulesEditModal()
    path = reverse("users_app:rule_edit", args=[1])

    def test_get_context_data(self):
        kwargs = {"pk": 1}
        response = UserRulesEditModal.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)


class UserRulesDeleteModalTest(UserRulesCreateTest):
    objview = UserRulesDeleteModal()
    path = reverse("users_app:rule_delete", args=[1])
    post_success = {}
    post_exception = {}

    def test_get_context_data(self):
        kwargs = {"pk": 1}
        response = UserRulesDeleteModal.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)


class UserViewsTest(TestCase):
    fixtures = [
        "users_fixtures.json",
    ]
    objview = UserList()
    path = reverse("users_app:user_list")
    post_success = {
        "email": "someone@example.com",
        "username": "someone",
        "password": "whatever",
        "repeat_pass": "whatever",
        "is_superuser": False,
        "is_staff": False,
        "is_active": True,
    }
    post_exception = {
        "email": "someone@example.com",
        "username": False,
        "password": "whatever",
        "is_superuser": False,
        "is_staff": False,
        "is_active": True,
    }
    post_duplicate = {
        "email": "email@something.com",
        "username": "random",
        "password": "Somepassword",
        "repeat_pass": "Somepassword",
        "is_superuser": False,
        "is_staff": False,
        "is_active": True,
    }

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.factory = RequestFactory()
        request = cls.factory.get(cls.path)
        request.user = cls.user
        cls.view = cls.objview
        cls.view.request = request

        cls.redirect = reverse("users_app:user_list")

    def test_get_context_data(self):
        kwargs = {}
        response = UserList.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)


class UserListTest(UserViewsTest):
    def test_get_queryset(self):
        queryset = self.view.get_queryset()
        data = User.objects.all().order_by("id")

        self.assertQuerysetEqual(queryset, data)


class UserCreateTest(UserViewsTest):
    objview = UserCreate()
    path = reverse("users_app:user_add")

    def test_successfull(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, self.post_success)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)

    def test_get_context_data(self):
        kwargs = {}
        response = UserCreate.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)

    def test_user_exception(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, self.post_exception)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)

    def test_user_duplicates(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, self.post_duplicate)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)


class UserEditModalTest(UserCreateTest):
    objview = UserEditModal()
    path = reverse("users_app:user_edit", args=[3])
    post_success = {
        "email": "someone@example.com",
        "username": "someone",
        "is_superuser": False,
        "is_staff": False,
        "is_active": False,
    }
    post_exception = {}
    post_duplicates = {
        "email": "someone@example.com",
        "username": "random",
        "is_superuser": False,
        "is_staff": False,
        "is_active": False,
    }

    def test_get_context_data(self):
        kwargs = {"pk": 3}
        response = UserEditModal.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)


class UserDeleteModalTest(UserCreateTest):
    objview = UserDeleteModal()
    path = reverse("users_app:user_delete", args=[3])
    post_success = {}
    post_exception = {}

    def test_get_context_data(self):
        kwargs = {"pk": 1}
        response = UserDeleteModal.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)


class UserLoginTest(TestCase):
    fixtures = [
        "users_fixtures.json",
    ]
    objview = UserLogin()
    path = reverse("users_app:login")
    credentials = {
        "username": "admin",
        "password": "Somepassword",
    }

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.factory = RequestFactory()
        request = cls.factory.get(cls.path)
        request.user = AnonymousUser()
        cls.view = cls.objview
        cls.view.request = request

        cls.redirect = reverse("users_app:user_list")

    def test_get_context_data(self):
        # kwargs = {"next": "/user/list"}
        kwargs = {}
        response = UserLogin.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)

    def test_successfull(self):
        response = self.client.post(self.path, self.credentials, follow=True)

        self.assertFalse(response.context["user"].is_active)
        # self.assertEqual(response.status_code, 302)
        # self.assertRedirects(response, self.redirect)

    def test_dispatch(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home_app:home_page"))


class UserLogoutTest(TestCase):
    fixtures = [
        "users_fixtures.json",
    ]
    objview = UserLogout()
    path = reverse("users_app:logout")

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.redirect = reverse("users_app:login")

    def test_get(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)


"""
class RegisterViewTest(TestCase):
    fixtures = [
        "users_fixtures.json",
    ]
    objview = RegisterView()
    path = reverse("users_app:register")
    post_success = {
        "username": "admin2",
        "email": "admin@example.com",
        "password": "Somepassword",
    }

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.factory = RequestFactory()
        request = cls.factory.get(cls.path)
        request.user = AnonymousUser()
        cls.view = cls.objview
        cls.view.request = request

        cls.redirect = reverse("users_app:login")

    def test_get_context_data(self):
        kwargs = {}
        response = RegisterView.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)

    def test_successfull(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, self.post_success, follow=True)
        pprint(response.__dict__)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)
"""


class UserProfileViewsTest(TestCase):
    fixtures = [
        "config_fixtures.json",
        "users_fixtures.json",
        "userprofile_fixture.json",
    ]
    objview = UserProfile()
    path = reverse("users_app:userprofile", args=["admin"])
    redirect = reverse("users_app:userprofile", args=["admin"])
    post_success = {
        "document_type": 1,
        "id_number": "11111",
        "name": "admin",
        "phone": "11111",
        "email": "admin@example.com",
        "address": "por ahí",
        "city": 1,
        "about_me": "soy yo",
    }
    post_invalid = {}

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.factory = RequestFactory()
        request = cls.factory.get(cls.path)
        request.user = cls.user
        cls.view = cls.objview
        cls.view.request = request
        cls.slug = "admin"


class UserProfileDetailTest(UserProfileViewsTest):
    def test_get_context_data(self):
        kwargs = {"slug": self.slug}
        response = UserProfileDetail.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)

    def test__other_get_context_data(self):
        kwargs = {"slug": "other"}
        response = UserProfileDetail.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)


class UserProfileCreateTest(UserProfileViewsTest):
    objview = UserProfileCreate()
    path = reverse("users_app:userprofile_add", args=["random"])
    redirect = reverse("users_app:userprofile", args=["random"])

    def test_successfull(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, self.post_success)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)

    def test_get_context_data(self):
        kwargs = {"slug": self.slug}
        response = UserProfileCreate.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)

    def test_userprofile_invalid(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, self.post_invalid)

        self.assertEqual(response.status_code, 200)

    def test_userprofile_exception(self):
        path = reverse("users_app:userprofile_add", args=["other"])
        self.client.force_login(user=self.user)
        response = self.client.post(path, self.post_success)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, path)


class UserProfileEditTest(UserProfileViewsTest):
    objview = UserProfileEdit()
    path = reverse("users_app:userprofile_edit", args=["admin"])
    # redirect = reverse("users_app:userprofile_edit", args=["admin"])
    post_success = {
        "document_type": 1,
        "id_number": "11111",
        "name": "random",
        "phone": "11111",
        "email": "random@example.com",
        "address": "por ahí",
        "city": 1,
        "about_me": "soy yo",
    }
    post_invalid = {}

    def test_get_context_data(self):
        kwargs = {"slug": "admin"}
        response = UserProfileEdit.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)

    def test_userprofile_invalid(self):
        self.redirect = reverse("users_app:userprofile_edit", args=["admin"])
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, self.post_invalid)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)

    def test_userprofile_exception(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, self.post_success)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)


class PreRegisterViewTest(TestCase):
    fixtures = ["users_fixtures.json"]
    path = reverse("users_app:register_choices")
    objview = PreRegisterView()

    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        request = cls.factory.get(cls.path)
        request.user = AnonymousUser()
        cls.view = cls.objview
        cls.view.request = request

    def test_get_context_data(self):
        kwargs = {}
        response = PreRegisterView.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)


class RegisterStudentViewTest(TestCase):
    fixtures = ["users_fixtures.json"]
    path = reverse("users_app:register_student")
    objview = RegisterStudentView()

    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        request = cls.factory.get(cls.path)
        request.user = AnonymousUser()
        cls.view = cls.objview
        cls.view.request = request

    def test_get_context_data(self):
        kwargs = {}
        response = RegisterStudentView.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)


class RegisterCompanyViewTest(TestCase):
    fixtures = ["users_fixtures.json"]
    path = reverse("users_app:register_company")
    objview = RegisterCompanyView()

    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        request = cls.factory.get(cls.path)
        request.user = AnonymousUser()
        cls.view = cls.objview
        cls.view.request = request

    def test_get_context_data(self):
        kwargs = {}
        response = RegisterCompanyView.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)


class CredentialsRecoverViewTest(TestCase):
    fixtures = ["users_fixtures.json"]
    path = reverse("users_app:credentials_recover")
    objview = CredentialsRecoverView()

    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        request = cls.factory.get(cls.path)
        request.user = AnonymousUser()
        cls.view = cls.objview
        cls.view.request = request

    def test_get_context_data(self):
        kwargs = {}
        response = CredentialsRecoverView.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)
