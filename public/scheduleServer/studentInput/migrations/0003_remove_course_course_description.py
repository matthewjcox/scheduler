# Generated by Django 2.1.2 on 2018-11-07 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentInput', '0002_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='course_description',
        ),
    ]