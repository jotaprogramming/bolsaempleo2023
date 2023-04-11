# python modules
from pprint import pprint

# django modules
from django.urls import reverse, reverse_lazy, resolve
from django.http import HttpResponse
from django.core.validators import validate_slug
from django.test import RequestFactory
from django.test import TestCase
from django.contrib.auth.models import User

from users.forms import (
    UserGroupForm,
    FormDelete,
    RestrictionForm,
    AppForm,
    RoleForm,
    UserRuleForm,
    UserPassForm,
    UserForm,
    RegisterForm,
    UserProfileModelForm,
)


from users.utils import get_form_errors

from config.models import Cities, Countries, Districts, Cities, DocumentType

from datetime import datetime


# Create your tests here.


class UserGroupFormTest(TestCase):
    def test_label_field(self):
        form = UserGroupForm()
        self.assertTrue(
            form.fields["group_name"].label == "Nombre"
            and form.fields["description"].label == "Descripción"
        )


class FormDeleteTest(TestCase):
    def test_required_field(self):
        form = FormDelete()
        self.assertTrue(form.fields["deleted_at"].required == False)


class RestrictionFormTest(TestCase):
    def test_label_field(self):
        form = RestrictionForm()
        self.assertTrue(
            form.fields["code"].label == "Código"
            and form.fields["name"].label == "Nombre"
            and form.fields["description"].label == "Descripción"
        )


class AppFormTest(TestCase):
    def test_label_field(self):
        form = AppForm()
        self.assertTrue(form.fields["description"].label == "Descripción")


class RoleFormTest(TestCase):
    def test_label_field(self):
        form = RoleForm()
        self.assertTrue(
            form.fields["role_name"].label == "Nombre"
            and form.fields["description"].label == "Descripción"
        )


class UserRuleFormTest(TestCase):
    def test_label_field(self):
        form = UserRuleForm()
        self.assertTrue(
            form.fields["user"].label == "Usuario"
            and form.fields["usergroup"].label == "Grupo"
            and form.fields["role"].label == "Rol"
        )


class UserFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form = UserPassForm()

    def test_label_field(self):
        self.assertTrue(
            self.form.fields["username"].label == "Usuario"
            and self.form.fields["email"].label == "Correo electrónico"
            and self.form.fields["password"].label == "Contraseña"
            and self.form.fields["is_superuser"].label == "¿Es superusuario?"
            and self.form.fields["is_staff"].label == "¿Es administrativo?"
            and self.form.fields["is_active"].label == "¿Es activo?"
        )

    def test_required_field(self):
        self.assertTrue(
            self.form.fields["is_superuser"].required == False
            and self.form.fields["is_staff"].required == False
            and self.form.fields["is_active"].required == False
        )

    def test_clean_repeat_pass(self):
        form_data = {"password": "pass", "repeat_pass": "pass1"}
        self.form = UserPassForm(data=form_data)

        self.assertFalse(self.form.is_valid())


class UserFormUpdateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form = UserForm()

    def test_label_field(self):
        self.assertTrue(
            self.form.fields["username"].label == "Usuario"
            and self.form.fields["email"].label == "Correo electrónico"
            and self.form.fields["is_superuser"].label == "¿Es superusuario?"
            and self.form.fields["is_staff"].label == "¿Es administrativo?"
            and self.form.fields["is_active"].label == "¿Es activo?"
        )

    def test_required_field(self):
        self.assertTrue(
            self.form.fields["is_superuser"].required == False
            and self.form.fields["is_staff"].required == False
            and self.form.fields["is_active"].required == False
        )


class RegisterFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form = RegisterForm()

    def test_label_field(self):
        self.assertTrue(
            self.form.fields["username"].label == "Usuario"
            and self.form.fields["email"].label == "Correo electrónico"
            and self.form.fields["password"].label == "Contraseña"
        )

    def test_clean_repeat_pass(self):
        form_data = {
            "username": "whatever",
            "email": "email@example.com",
            "password": "pass",
            "repeat_pass": "pass1",
        }
        self.form = RegisterForm(data=form_data)

        self.assertFalse(self.form.is_valid())


class UserProfileModelFormTest(TestCase):
    def test_required_field(self):
        form = UserProfileModelForm()
        self.assertTrue(form.fields["about_me"].required == False)
