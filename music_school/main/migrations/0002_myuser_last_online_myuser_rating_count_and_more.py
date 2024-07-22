# Generated by Django 5.0.4 on 2024-07-16 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='last_online',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Последний онлайн'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='rating_count',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='myuser',
            name='total_rating',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]