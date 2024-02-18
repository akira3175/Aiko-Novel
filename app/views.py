from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'app/home.html')
def search(request):
    keywords = request.GET.get('keywords')
    return render(request, 'app/search.html', {'keywords': keywords})