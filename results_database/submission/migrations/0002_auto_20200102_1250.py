# Generated by Django 2.0 on 2020-01-02 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_name',
            field=models.CharField(default=None, max_length=50, primary_key=True, serialize=False),
        ),
    ]
