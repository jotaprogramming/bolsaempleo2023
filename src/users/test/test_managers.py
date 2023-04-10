# python modules
from pprint import pprint

# django modules
from django.urls import reverse, reverse_lazy, resolve
from django.http import HttpResponse
from django.core.validators import validate_slug
from django.test import RequestFactory
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.timezone import now

from users.models import UserRules
from users.managers import TraitManager


from users.utils import get_form_errors

from config.models import Cities, Countries, Districts, Cities, DocumentType

from datetime import datetime, timezone


class UserRulesManagerTest(TestCase):
    fixtures = [
        "users_fixtures.json",
        "apps_fixtures.json",
        "restrictions_fixtures.json",
        "roles_fixtures.json",
        "rules_fixtures.json",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.rules = UserRules.objects.order_by().values()

    def test_get_nums(self):
        data_expected = [
            {
                "id": 1,
                "user_id": 1,
                "num_apps": 1,
                "num_restrictions": 1,
                "num_roles": 1,
                "created_at": datetime(
                    2023, 3, 2, 19, 29, 50, 239305, tzinfo=timezone.utc
                ),
                "updated_at": None,
                "deleted_at": None,
            }
        ]

        self.assertQuerysetEqual(self.rules, data_expected)
