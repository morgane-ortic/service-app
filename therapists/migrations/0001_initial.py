# Generated by Django 5.1.4 on 2025-01-23 10:21

import django.db.models.deletion
import multiselectfield.db.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Therapist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(choices=[('W', 'Woman'), ('M', 'Man'), ('O', 'Other')], max_length=1)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('street', models.CharField(blank=True, max_length=255, null=True)),
                ('number', models.CharField(blank=True, max_length=10, null=True)),
                ('postcode', models.CharField(blank=True, max_length=20, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('picture', models.ImageField(upload_to='therapist_pictures/')),
                ('qualifications', models.CharField(blank=True, max_length=1000, null=True)),
                ('specialties', models.CharField(blank=True, max_length=1000, null=True)),
                ('years_xp', models.IntegerField()),
                ('accepted_customer_groups', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('single', 'Single'), ('couple', 'Couple'), ('group', 'Group')], max_length=19)),
                ('provided_equipment', models.TextField(blank=True, max_length=1000, null=True)),
                ('required_equipment', models.TextField(blank=True, max_length=1000, null=True)),
                ('pronouns', models.CharField(default='Not Specified', max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('issuing_org', models.CharField(blank=True, max_length=100, null=True)),
                ('issuing_date', models.DateField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('certif_file', models.FileField(upload_to='uploads/')),
                ('therapist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certification', to='therapists.therapist')),
            ],
        ),
        migrations.CreateModel(
            name='TherapistService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_price', models.DecimalField(decimal_places=2, default=60, max_digits=6)),
                ('prices', models.JSONField(default=list)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='therapist_services', to='core.service')),
                ('therapist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='therapists.therapist')),
            ],
        ),
    ]
