# Generated by Django 4.2.6 on 2023-10-19 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='calories',
            field=models.PositiveIntegerField(help_text='Total Number of calories in an entry'),
        ),
    ]
