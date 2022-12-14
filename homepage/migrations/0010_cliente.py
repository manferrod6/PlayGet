# Generated by Django 4.1.3 on 2022-11-23 15:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0009_carro_id_carro'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_completo', models.TextField(max_length=60)),
                ('direccion', models.TextField(max_length=1000)),
                ('codigo_postal', models.CharField(max_length=5, validators=[django.core.validators.RegexValidator(code='nomatch', message='Length has to be 5', regex='\x08\\d{5}\x08')])),
                ('correo', models.EmailField(max_length=50)),
            ],
        ),
    ]
