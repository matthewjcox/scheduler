# Generated by Django 2.1.2 on 2019-03-14 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentInput', '0020_auto_20190228_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='rmNum',
            field=models.CharField(max_length=15),
        ),
    ]
