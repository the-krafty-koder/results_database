# Generated by Django 2.0 on 2019-12-30 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='institution_name',
            field=models.CharField(max_length=50),
        ),
    ]
