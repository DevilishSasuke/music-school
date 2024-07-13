from django.shortcuts import render
from .forms import BugForm

from django.core.mail import send_mail

from dotenv import load_dotenv
from os import getenv

load_dotenv()

# Create your views here.
def home(request):
  return render(request, 'home.html')

def profile(request):
  return render(request, 'layout.html')

def calendar(request):
  pass

def chat(request):
  pass

def lessons(request):
  pass

def rating(request):
  pass

def pay(request):
  pass

def bug(request):
  if  request.method == 'POST':
    form = BugForm(request.POST)
    if form.is_valid():
      user_email = form.cleaned_data['user_email']
      user_msg = form.cleaned_data['text']
      send_bug_report(user_email, user_msg)

  form = BugForm()

  data = {
    'title': 'Сообщить об ошибке',
    'form': form,
  }

  return render(request, 'bug.html', data)



def send_bug_report(email, text):
  subject = "Bug report"
  message = f'Bug report from {email}:\n\n {text}'
  sender = getenv("CORPORATE_EMAIL")
  recipient = [getenv("ADMIN_EMAIL")]

  send_mail(subject, message, sender, recipient)
  