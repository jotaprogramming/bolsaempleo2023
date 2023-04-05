# Generated by Django 4.1.7 on 2023-03-13 22:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="usergroups",
            name="code",
            field=models.CharField(
                default="000", max_length=3, unique=True, verbose_name="user group code"
            ),
            preserve_default=False,
        ),
    ]
