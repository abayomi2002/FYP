# Generated by Django 5.0.6 on 2024-08-23 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='female', max_length=10),
        ),
    ]
