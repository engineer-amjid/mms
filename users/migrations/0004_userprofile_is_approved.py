# Generated by Django 5.1.4 on 2024-12-17 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userprofile_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_approved',
            field=models.BooleanField(default=False, verbose_name='Is Approved'),
        ),
    ]
