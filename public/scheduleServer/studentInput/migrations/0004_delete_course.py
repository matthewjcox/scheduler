# Generated by Django 2.1.2 on 2018-11-07 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentInput', '0003_remove_course_course_description'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Course',
        ),
    ]
