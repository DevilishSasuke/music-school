from django.shortcuts import render

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
  return render(request, 'bug.html')