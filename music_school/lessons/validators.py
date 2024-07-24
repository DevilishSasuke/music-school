from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_file_size(file):
  limit = 1024 * 1024
  if file.size > limit:
    raise ValidationError(f"Max file size is {limit} KB")
  
def validate_date_time(value):
  if value <= timezone.now():
    raise ValidationError("Date and time can't be less than NOW")