# Generated by Django 5.0.4 on 2024-07-24 20:44

import django.core.validators
import lessons.models
import lessons.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0002_alter_lesson_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=lessons.models.lessons_file_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'bmp', 'doc', 'docx', 'pdf', 'txt', 'ppt', 'pptx', 'md', 'mp3', 'wav', 'flac', 'm4a', 'mp4', 'mov', 'avi', 'mkv', 'zip', 'rar']), lessons.validators.validate_file_size]),
        ),
    ]