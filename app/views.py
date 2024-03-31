from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from app.models import Book, User, Category
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout # thu vien xac thuc
from django.contrib.auth.models import User
from django.contrib import messages # thu vien thong bao
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')

        if password == repassword:
            myuser = User.objects.create_user(username=username, email=email, password=password)
            myuser.save()
            messages.success(request, "Your account has been registered")
            return redirect('home')
        else:
            messages.error(request, "Passwords do not match")

    return redirect('home')

def loginPage(request):
    if request.user.is_authenticated:
        return render(request, 'app/home.html', {'name': request.user.username})
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password is incorrect!")

    return redirect('home')

def logoutPage(request):
    logout(request)
    return redirect('home')
    
def home(request):
    novels = Book.objects.all()
    return render(request, 'app/home.html', {'novels': novels}) 
    
def search(request):
    title = request.GET.get('title')
    author = request.GET.get('author')
    selectcategory   = request.GET.get('selectcategory ')
    rejectcategory  = request.GET.get('rejectcategory ')
    status = request.GET.get('status')
    if title is not None and title != '':
        queryset = Book.objects.all()
    else:
        return render(request, 'app/search.html')

    if title:
        queryset = queryset.filter(title=title)

    if author:
        queryset = queryset.filter(author=author)

    if selectcategory :
        selectcategory  = selectcategory .split(',')
        queryset = queryset.filter(category__in=selectcategory )

    if rejectcategory :
        rejectcategory  = rejectcategory .split(',')
        queryset = queryset.exclude(category__in=rejectcategory )
    # if status:
    #     queryset = queryset.filter(status=status)
    results = queryset.distinct()
    return render(request, 'app/search.html', {'keywords': title,'matched_books': results})

def transTeam(request):
    return render(request, 'app/transteam.html')

def novelOfTransTeam(request):
    return render(request, 'app/novel-of-trans.html')

def novelWorks(request):
    categories = Category.objects.all()
    return render(request, 'app/novelworks.html', {'categories': categories})

@csrf_exempt
def saveBook(request):
    if request.method == 'POST':
        # Nhận dữ liệu từ yêu cầu POST
        id = int(request.POST.get('novelid', -1))  # Chuyển đổi id sang kiểu int
        title = request.POST.get('title')
        author = request.POST.get('author')
        artist = request.POST.get('artist')
        novelTransTeam = request.POST.get('novelTransTeam')
        category = request.POST.get('category')
        description = request.POST.get('description')
        checkboxChecked = request.POST.get('checkboxChecked')
        isCompleted = checkboxChecked.lower() == 'true' if checkboxChecked else False
        image = request.FILES.get('image')

        # Kiểm tra xem id có phải là -1 (tạo mới) hay không
        if id == -1:
            # Tạo mới đối tượng Book
            new_book = Book.objects.create(
                title=title,
                author=author,
                artist=artist,
                workerid=novelTransTeam,
                category=category,
                description=description,
                isCompleted=isCompleted,
                img=image,
                dateUpload=timezone.now(),
                dateUpdate=timezone.now()
            )
            # Trả về phản hồi thành công
            return redirect('novel-of-trans-team')
        else:
            # Cập nhật thông tin của đối tượng Book đã tồn tại
            try:
                existing_book = Book.objects.get(id=id)
                existing_book.title = title
                existing_book.author = author
                existing_book.artist = artist
                existing_book.workerid = novelTransTeam
                existing_book.category = category
                existing_book.description = description
                existing_book.isCompleted = isCompleted
                existing_book.dateUpdate = timezone.now()
                if image:
                    existing_book.img = image
                existing_book.save()
                # Trả về phản hồi thành công
                return redirect('novel-of-trans-team')
            except Book.DoesNotExist:
                return JsonResponse({'error': 'Không tìm thấy đối tượng Book với id đã cho.'}, status=404)

    else:
        return JsonResponse({'error': 'Yêu cầu không hợp lệ.'}, status=405)