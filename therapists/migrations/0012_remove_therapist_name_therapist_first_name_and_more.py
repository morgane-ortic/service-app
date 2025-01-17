# Generated by Django 5.1.4 on 2025-01-17 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('therapists', '0011_therapist_age_therapist_pronouns'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='therapist',
            name='name',
        ),
        migrations.AddField(
            model_name='therapist',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='therapist',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
