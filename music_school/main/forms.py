from django.forms import Form, ModelForm, CharField, \
  TextInput, Textarea, \
  DateField, DateInput, \
  IntegerField, HiddenInput
from .models import MyUser

class UserInfoForm(ModelForm):
  last_name = CharField(
    required=False,
    widget=
    TextInput(attrs={
      "id": "last_name",
      "type": "text",
      "placeholder": "Фамилия",
      })
    )
  
  first_name = CharField(
    required=False,
    widget=
    TextInput(attrs={
      "id": "first_name",
      "type": "text",
      "placeholder": "Имя",
      })
    )
  
  middle_name = CharField(
    required=False,
    widget=
    TextInput(attrs={
      "id": "middle_name",
      "type": "text",
      "placeholder": "Отчество",
      })
    )
  
  email = CharField(
    required=False,
    widget=
    TextInput(attrs={
      "id": "email",
      "type": "email",
      "placeholder": "example@eg.com",
      })
    )
  
  phone = CharField(
    required=False,
    widget=
    TextInput(attrs={
      "id": "phone",
      "type": "text",
      "placeholder": "+7(900)-123-45-67",
      # pattern for russian phone number
      "pattern": r"^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$"
      })
    )
  
  birth_date = DateField(
    required=False,
    widget=
    TextInput(attrs={
      "id": "birth_date",
      "type": "date",
      })
    )


  class Meta:
    model = MyUser
    fields = ["last_name", "first_name", "middle_name", 
              "email", "phone", "birth_date"]

class RateForm(Form):
  rating = IntegerField(
      min_value=1,
      max_value=5,
      widget=HiddenInput()
    )

class BugForm(Form):
  user_email = CharField(
    widget=
    TextInput(attrs={
      "type": "email",
      "placeholder": "example@eg.com",
    })
  )
  text = CharField(
    widget=
    Textarea(attrs={
      "rows": 5,
    })
  )