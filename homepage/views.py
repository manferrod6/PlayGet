from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'homepage/home.html')

def index(request):
    return render(request, 'homepage/index.html')

def catalogo(request):
    return render(request, 'homepage/catalogo.html')