from django.db import models
from django.db.models import Q, F, Count

from django.contrib.auth.models import BaseUserManager

# class UserManager(BaseUserManager, models.Manager):
#     def _create_user(self, username, email, password, is_active, **extra_fields):
#         user = self.model(
#             username=username,
#             email=email,
#             is_active=is_active,
#             **extra_fields
#         )
#         user.set_password(password)
#         user.save(using=self.db)
#         return user
    
#     def create_user(self, username, email, password=None, **extra_fields):
#         return self._create_user(username, email, password, True, **extra_fields)

#     def create_superuser(self, username, email=None, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)

#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True.")
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True.")

#         return self._create_user(username, email, password, **extra_fields)

class RulesManager(models.Manager):
    def get_nums(self):
        return self.annotate(
            num_apps=Count('app', distinct=True),
            num_roles=Count('role', distinct=True),
            num_restrictions=Count('restriction', distinct=True)
        ).order_by("id")