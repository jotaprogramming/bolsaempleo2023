# python modules
from pprint import pprint

# django modules
from django.urls import reverse, reverse_lazy, resolve
from django.http import HttpResponse
from django.core.validators import validate_slug
from django.test import RequestFactory
from django.test import TestCase
from django.contrib.auth.models import User, AnonymousUser
from django.urls import path

from users.models import (
    UserGroups,
    Restrictions,
    Apps,
    Roles,
    Rules,
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
    RuleList,
    RuleCreate,
    RuleEditModal,
    RuleDeleteModal,
    UserList,
    UserCreate,
    UserEditModal,
    UserDeleteModal,
    UserLogin,
    UserLogout,
    RegisterView,
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
    model = UserGroupList()
    path = reverse("users_app:usergroup_list")

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.factory = RequestFactory()
        request = cls.factory.get(cls.path)
        request.user = cls.user
        cls.view = cls.model
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
    model = UserGroupCreate()
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
    model = UserGroupEditModal()
    path = reverse("users_app:usergroup_edit", args=[1])

    def test_get_context_data(self):
        kwargs = {"pk": 1}
        response = UserGroupEditModal.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)


class UserGroupDeleteModalTest(UserGroupCreateTest):
    fixtures = ["users_fixtures.json", "usergroups_fixtures.json"]
    model = UserGroupDeleteModal()
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
    model = RestrictionList()
    path = reverse("users_app:restriction_list")

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.factory = RequestFactory()
        request = cls.factory.get(cls.path)
        request.user = cls.user
        cls.view = cls.model
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
    model = RestrictionCreate()
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
    model = RestrictionEditModal()
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
    model = RestrictionDeleteModal()
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
    model = AppList()
    path = reverse("users_app:app_list")

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.factory = RequestFactory()
        request = cls.factory.get(cls.path)
        request.user = cls.user
        cls.view = cls.model
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
    model = AppEditModal()
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
    model = RoleList()
    path = reverse("users_app:role_list")

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.factory = RequestFactory()
        request = cls.factory.get(cls.path)
        request.user = cls.user
        cls.view = cls.model
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
        data = Roles.objects.all().order_by("id")

        self.assertQuerysetEqual(queryset, data)


class RoleCreateTest(RoleViewsTest):
    fixtures = ["users_fixtures.json", "roles_fixtures.json"]
    model = RoleCreate()
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
    model = RoleEditModal()
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
    model = RoleDeleteModal()
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


class RuleViewsTest(TestCase):
    fixtures = [
        "users_fixtures.json",
        "apps_fixtures.json",
        "restrictions_fixtures.json",
        "roles_fixtures.json",
        "rules_fixtures.json",
    ]
    model = RuleList()
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
        cls.view = cls.model
        cls.view.request = request

        cls.redirect = reverse("users_app:rule_list")

    def test_get_context_data(self):
        kwargs = {}
        response = RuleList.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)


class RuleListTest(RuleViewsTest):
    def test_get_queryset(self):
        queryset = self.view.get_queryset()
        data = Rules.objects.all().order_by("id")

        self.assertQuerysetEqual(queryset, data)


class RuleCreateTest(RuleViewsTest):
    model = RuleCreate()
    path = reverse("users_app:rule_add")

    def test_successfull(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, self.post_success)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)

    def test_get_context_data(self):
        kwargs = {}
        response = RuleCreate.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)

    def test_rule_exception(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.path, self.post_exception)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)


class RuleEditModalTest(RuleCreateTest):
    model = RuleEditModal()
    path = reverse("users_app:rule_edit", args=[1])

    def test_get_context_data(self):
        kwargs = {"pk": 1}
        response = RuleEditModal.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)


class RuleDeleteModalTest(RuleCreateTest):
    model = RuleDeleteModal()
    path = reverse("users_app:rule_delete", args=[1])
    post_success = {}
    post_exception = {}

    def test_get_context_data(self):
        kwargs = {"pk": 1}
        response = RuleDeleteModal.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)


class UserViewsTest(TestCase):
    fixtures = [
        "users_fixtures.json",
    ]
    model = UserList()
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
        cls.view = cls.model
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
    model = UserCreate()
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
    model = UserEditModal()
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
    model = UserDeleteModal()
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
    model = UserLogin()
    path = reverse("users_app:login")
    post_success = {
        "username": "admin",
        "password": "Somepassword",
    }
    post_exception = {
        "username": "admin",
        "password": "whatever",
    }

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.factory = RequestFactory()
        request = cls.factory.get(cls.path)
        # request.user = AnonymousUser
        cls.view = cls.model
        cls.view.request = request

        cls.redirect = reverse("users_app:user_list")

    def test_get_context_data(self):
        kwargs = {"next": "/user/list"}
        response = UserLogin.as_view()(self.view.request, **kwargs)
        print("response: ", response.status_code)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)

    def test_successfull(self):
        # self.client.request.user = AnonymousUser
        response = self.client.post(self.path, self.post_success)
        # pprint(response.__dict__)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)

    def test_get_context_data(self):
        kwargs = {}
        response = UserLogin.as_view()(self.view.request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data)

    def test_user_exception(self):
        # self.client.force_login(user=self.user)
        response = self.client.post(self.path, self.post_exception)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect)
