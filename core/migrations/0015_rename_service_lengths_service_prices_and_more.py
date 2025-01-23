# Generated by Django 5.1.4 on 2025-01-20 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_booking_service'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='service_lengths',
            new_name='prices',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='price',
        ),
        migrations.RemoveField(
            model_name='service',
            name='service_types',
        ),
        migrations.AddField(
            model_name='booking',
            name='base_price',
            field=models.DecimalField(decimal_places=2, default=50, max_digits=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='prices',
            field=models.JSONField(default=list),
        ),
    ]
