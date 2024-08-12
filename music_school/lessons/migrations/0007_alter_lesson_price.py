# Generated by Django 5.0.4 on 2024-07-30 16:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0006_lesson_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]