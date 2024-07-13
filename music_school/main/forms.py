from django.forms import Form, CharField, TextInput, Textarea

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