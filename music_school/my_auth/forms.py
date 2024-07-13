from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import CharField, TextInput, PasswordInput

class RegistrationForm(UserCreationForm):
  user_email = CharField(widget=
    TextInput(attrs={
        "id": "email",
        "name": "user_email",
        "placeholder": "myemail@gmail.com",
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

  class Meta:

        model = User
        fields = [
            "user_email",
            "password1",
            "password2",
        ]

class LoginForm(AuthenticationForm):
  user_email = CharField(widget=
    TextInput(attrs={
        "id": "email",
        "name": "user_email",
        "placeholder": "myemail@gmail.com",
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

  class Meta:
     fields = [
        "user_email",
        "password"
     ]