# Generated by Django 2.1.2 on 2018-11-07 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentInput', '0005_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_text', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Course',
        ),
    ]
