# Generated by Django 2.1.2 on 2018-11-08 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentInput', '0010_auto_20181108_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_credits',
            field=models.FloatField(default=0.5),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_weight',
            field=models.FloatField(default=0.5),
        ),
    ]
