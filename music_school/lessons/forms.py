from django.forms import ModelForm, DateTimeInput, Textarea

from .models import Lesson


class LessonForm(ModelForm):
  class Meta:
    model = Lesson
    fields = ["teacher", "date", "title", "description", "file"]
    widgets = {
            'date': DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': Textarea(attrs={'rows': '3'}),
        }