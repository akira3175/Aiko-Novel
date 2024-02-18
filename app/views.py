from django.shortcuts import render
from django.http import HttpResponse
from app.models import Book
# Create your views here.
def home(request):
    return render(request, 'app/home.html')
def search(request):
    keywords = request.GET.get('keywords')
    matched_books = []
    all_book = Book.objects.all()
    if all_book:
        for book in all_book:
            if keywords.lower() in book.title.lower():
                matched_books.append(book)
    return render(request, 'app/search.html', {'keywords': keywords,'matched_books': matched_books})