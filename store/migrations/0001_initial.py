# Generated by Django 5.1 on 2024-08-14 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Item",
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
                ("key", models.CharField(db_index=True, max_length=100, unique=True)),
                ("value", models.TextField()),
                ("expires_at", models.DateTimeField(db_index=True)),
            ],
        ),
    ]
