# Generated by Django 4.2.7 on 2023-11-17 13:57

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_profile_delete_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phonenumber',
            field=models.IntegerField(unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid')]),
        ),
    ]
