# Generated by Django 4.2 on 2023-06-21 08:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Application",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("email", models.EmailField(blank=True, max_length=255, null=True)),
                (
                    "resume",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="resumes/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["pdf"]
                            )
                        ],
                    ),
                ),
                ("submitted_on", models.DateField(auto_now=True)),
                ("posted_by", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("accepted", "Accepted"),
                            ("rejected", "Rejected"),
                        ],
                        default="pending",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "company_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "company_website",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "company_location",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "logo",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="logo/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["png", "jpg", "jpeg"]
                            )
                        ],
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Job",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("company_name", models.CharField(max_length=200)),
                ("company_website", models.CharField(max_length=200)),
                (
                    "image",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="image/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["png", "jpg", "jpeg"]
                            )
                        ],
                    ),
                ),
                ("location", models.CharField(max_length=201)),
                ("salary", models.CharField(max_length=10)),
                ("created_at", models.DateField(auto_now_add=True)),
                ("application_valid", models.DateField(blank=True, null=True)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("freelancer", "Freelancer"),
                            ("parttime", "Parttime"),
                            ("fulltime", "Fulltime"),
                            ("intern", "Intern"),
                        ],
                        default="fulltime",
                    ),
                ),
                ("modified_at", models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message", models.CharField(blank=True, max_length=1055, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("accepted", "Accepted"),
                            ("rejected", "Rejected"),
                        ],
                        default="pending",
                    ),
                ),
                (
                    "application",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="jobs.application",
                    ),
                ),
            ],
        ),
    ]