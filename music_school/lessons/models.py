from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
import datetime

from .validators import validate_file_size, validate_date_time

extensions = [
   "jpg", "jpeg", "png", "gif", "bmp", #image files 
   "doc", "docx", "pdf", "txt", "ppt", "pptx", "md", # default docs
   "mp3", "wav", "flac", "m4a", # audio files
   "mp4", "mov", "avi", "mkv", # video files
   "zip", "rar", # archived files
   "html", "htm", "xml", "json" # files for meta data
]

def lessons_file_path(instance, filename):
  return f'lessons_files/{instance.id}/{filename}'

class Lesson(models.Model):
  teacher = models.CharField(max_length=150, blank=True, null=False)
  date = models.DateTimeField(blank=False, null=False, validators=[validate_date_time])
  title = models.CharField(max_length=100, blank=False, null=False)
  description = models.TextField(blank=True, null=True)
  file = models.FileField(upload_to=lessons_file_path, null=True, blank=True,
                          validators=[FileExtensionValidator(allowed_extensions=extensions),
                                      validate_file_size])

  @property
  def get_date(self):
     return self.date.date()
  
  @property
  def get_time(self):
    return self.date.time()
  
  @property
  def file_path(self, filename):
    return f'lessons_files/{self.id}/{filename}'
  
  def get_lesson_by_id(lesson_number):
    try:
        lesson = Lesson.objects.get(id=lesson_number)
        return lesson
    except Lesson.DoesNotExist:
        return None
    
  def get_lessons_by_teacher(username):
    try:
      lessons = Lesson.objects.filter(teacher=username, date__gt=timezone.now())
      return lessons
    except Lesson.DoesNotExist:
      return None
    
  def get_lessons_by_subscriptions(username):
    teacher_list = None # get_teacher_list()

    return None

  def __str__(self):
    return f'{self.id}: {self.title} - {self.teacher} - {self.date}'
