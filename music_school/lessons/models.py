from django.db import models


def lessons_file_path(instance, filename):
  return f'lessons_files/{instance.id}/{filename}'

class Lesson(models.Model):
  teacher = models.CharField(max_length=150, blank=True, null=False)
  date = models.DateTimeField(blank=False, null=False)
  title = models.CharField(max_length=100, blank=False, null=False)
  description = models.TextField(blank=True, null=True)
  file = models.FileField(upload_to=lessons_file_path, null=True, blank=True)

  @property
  def get_date(self):
     return self.date.date()
  
  @property
  def get_time(self):
    return self.date.time()

  def __str__(self):
    return f'{self.title} - {self.teacher} - {self.date}'
