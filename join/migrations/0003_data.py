# Generated by Django 3.0.6 on 2020-07-15 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('join', '0002_auto_20200714_1605'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise', models.CharField(max_length=500)),
                ('amount', models.IntegerField(default=0)),
            ],
        ),
    ]
