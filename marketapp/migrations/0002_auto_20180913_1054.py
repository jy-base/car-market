# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-09-13 10:54
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='number_of_seats',
            field=models.IntegerField(default=4, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='car',
            name='price',
            field=models.IntegerField(default=100, validators=[django.core.validators.MinValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='car',
            name='stock_count',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='car',
            name='year',
            field=models.IntegerField(default=2018, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='comment',
            name='rating',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)]),
        ),
    ]