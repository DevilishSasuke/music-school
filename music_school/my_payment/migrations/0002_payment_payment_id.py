# Generated by Django 5.0.4 on 2024-08-11 19:50

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
