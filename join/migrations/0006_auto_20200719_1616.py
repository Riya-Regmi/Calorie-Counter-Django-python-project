# Generated by Django 3.0.6 on 2020-07-19 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('join', '0005_remove_data_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformation',
            name='calculation_coffee',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='userinformation',
            name='calculation_exercise',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='userinformation',
            name='calculation_water',
            field=models.TextField(),
        ),
    ]
