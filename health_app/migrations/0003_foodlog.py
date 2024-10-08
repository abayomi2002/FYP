# Generated by Django 5.0.6 on 2024-08-24 04:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_app', '0002_customuser_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(max_length=255)),
                ('calories', models.PositiveIntegerField(help_text='Calories in the portion')),
                ('date_logged', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food_logs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
