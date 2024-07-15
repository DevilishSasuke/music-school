from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import CharField, TextInput, PasswordInput, ChoiceField

from main.models import MyUser


class RegistrationForm(UserCreationForm):
  username = CharField(widget=
    TextInput(attrs={
        "id": "username",
        "name": "username",
        "placeholder": "username",
      })
  )

  password1 = CharField(widget=
    PasswordInput(attrs={
                "type": "password",
                "id": "password1",
                "name": "password1",
                "placeholder": "password",
      })
  )
    
  password2 = CharField(widget=
    PasswordInput(attrs={
              "type": "password",
              "id": "password2",
              "name": "password2",
              "placeholder": "repeat password",
      })
  )

  ROLE_CHOICES = [
        (False, 'Ученик'),
        (True, 'Учитель'),
    ]
  is_teacher = ChoiceField(choices=ROLE_CHOICES)

  class Meta:

        model = MyUser
        fields = [
            "username",
            "password1",
            "password2",
            "is_teacher",
        ]

class LoginForm(AuthenticationForm):
  username = CharField(widget=
    TextInput(attrs={
        "id": "username",
        "name": "username",
        "placeholder": "username",
      })
  )

  password = CharField(widget=
    PasswordInput(attrs={
                "type": "password",
                "id": "password",
                "name": "password",
                "placeholder": "password",
      })
  )