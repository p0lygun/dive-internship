# Generated by Django 4.2.6 on 2023-10-22 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_manageruser_customuser_ptr_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='calories_per_day',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
