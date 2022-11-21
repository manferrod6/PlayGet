from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'homepage/home.html')

def index(request):
    return render(request, 'homepage/index.html')

def sobre_nosotros(request):
    return render(request, 'homepage/sobre_nosotros.html')


