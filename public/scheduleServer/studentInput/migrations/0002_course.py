# Generated by Django 2.1.2 on 2018-11-07 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentInput', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=100)),
                ('course_id', models.IntegerField(default=0)),
                ('course_description', models.CharField(max_length=1000)),
            ],
        ),
    ]
