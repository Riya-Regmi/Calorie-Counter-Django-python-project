# Generated by Django 3.0.6 on 2020-07-15 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('join', '0004_data_weight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='weight',
        ),
    ]
