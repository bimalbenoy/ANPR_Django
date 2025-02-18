# Generated by Django 4.2.18 on 2025-02-16 05:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0002_residents'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='residents',
            name='Plate_number',
        ),
        migrations.AddField(
            model_name='residents',
            name='category',
            field=models.CharField(choices=[('Resident', 'Resident'), ('Visitor', 'Visitor'), ('Criminal', 'Criminal')], default='Resident', max_length=10),
        ),
        migrations.AddField(
            model_name='residents',
            name='owner_name',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='residents',
            name='registered_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='residents',
            name='resident_address',
            field=models.TextField(default='Not Provided'),
        ),
        migrations.AddField(
            model_name='residents',
            name='vehicle_number',
            field=models.CharField(default=django.utils.timezone.now, max_length=20, unique=True),
            preserve_default=False,
        ),
    ]
