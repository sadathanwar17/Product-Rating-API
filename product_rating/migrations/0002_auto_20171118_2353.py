# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-18 18:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_rating', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_table',
            name='product_quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product_table',
            name='product_ratings',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product_table',
            name='product_status',
            field=models.IntegerField(default=0),
        ),
    ]
