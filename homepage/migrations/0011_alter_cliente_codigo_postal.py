# Generated by Django 4.1.3 on 2022-11-23 15:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0010_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='codigo_postal',
            field=models.CharField(max_length=6, validators=[django.core.validators.RegexValidator(code='nomatch', message='Length has to be 5', regex='/\x08\\d{5}\x08/g')]),
        ),
    ]
