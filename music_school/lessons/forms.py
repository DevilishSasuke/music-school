from django.forms import ModelForm, DateTimeInput, Textarea

from .models import Lesson


class LessonForm(ModelForm):
  class Meta:
    model = Lesson
    fields = ["teacher", "date", "title", "description", "price", "file"]
    widgets = {
            'date': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'description': Textarea(attrs={'rows': '3'}),
        }