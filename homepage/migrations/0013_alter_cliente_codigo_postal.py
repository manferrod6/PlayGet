# Generated by Django 4.1.3 on 2022-11-23 15:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0012_alter_cliente_codigo_postal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='codigo_postal',
            field=models.CharField(max_length=5, validators=[django.core.validators.RegexValidator(code='nomatch', message='Length has to be 5', regex='\\d{5}')]),
        ),
    ]
