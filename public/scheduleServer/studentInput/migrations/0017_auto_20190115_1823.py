# Generated by Django 2.1.2 on 2019-01-15 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentInput', '0016_auto_20190115_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_id',
            field=models.CharField(max_length=12),
        ),
    ]
