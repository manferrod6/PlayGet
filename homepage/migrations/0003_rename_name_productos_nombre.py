# Generated by Django 4.1.3 on 2022-11-19 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_alter_productos_cantidad_alter_productos_precio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productos',
            old_name='name',
            new_name='nombre',
        ),
    ]
