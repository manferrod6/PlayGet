# Generated by Django 4.1.3 on 2022-11-19 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0004_rename_productos_producto'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='categoria',
            field=models.TextField(default='pipo', max_length=200),
            preserve_default=False,
        ),
    ]
