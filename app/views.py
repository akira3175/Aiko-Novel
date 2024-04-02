from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from app.models import Book, UserInfo, Category, Role
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
        date_join = timezone.now()

        if password == repassword:
            # Tạo một người dùng mới
            myuser = User.objects.create_user(
                username=username, 
                email=email, 
                password=password,
            )

            # Tạo một đối tượng UserInfo và liên kết với người dùng mới
            UserInfo.objects.create(username=myuser, full_name=myuser.username, date_join=date_join, role_id = -999)

            messages.success(request, "Your account has been registered")
            return redirect('home')
        else:
            messages.error(request, "Passwords do not match")

    return redirect('home')

def checkUsername(request):
    if request.method == 'GET' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        username = request.GET.get('username', '').strip()
        if username:
            try:
                if User.objects.filter(username__iexact=username).exists():
                    return JsonResponse({'is_taken': True})
                else:
                    return JsonResponse({'is_taken': False})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Yêu cầu không hợp lệ.'}, status=400)
    else:
        return JsonResponse({'error': 'Yêu cầu không hợp lệ hoặc không phải là AJAX.'}, status=400)

def checkEmail(request):
    if request.method == 'GET' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        email = request.GET.get('email', '').strip()
        if email:
            try:
                if User.objects.filter(email__iexact=email).exists():
                    return JsonResponse({'is_taken': True})
                else:
                    return JsonResponse({'is_taken': False})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Yêu cầu không hợp lệ.'}, status=400)
    else:
        return JsonResponse({'error': 'Yêu cầu không hợp lệ hoặc không phải là AJAX.'}, status=400)


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
    keywords = request.GET.get('keywords')
    matched_books = []
    all_book = Book.objects.all()
    if all_book:
        for book in all_book:
            if keywords.lower() in book.title.lower():
                matched_books.append(book)
    return render(request, 'app/search.html', {'keywords': keywords,'matched_books': matched_books})

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
    
def profile(request, username):
    userInfo, created = UserInfo.objects.get_or_create(username__username=username) 
    return render(request, 'app/profile.html', {'userInfo': userInfo})

from django.shortcuts import get_object_or_404

def saveBackground(request):
    if request.method == 'POST':
        if request.user.is_authenticated:  # Đảm bảo người dùng đã xác thực
            username = request.user.username
            background_image = request.FILES.get('backgroundImage')
            scroll_position = request.POST.get('scrollPosition')
            
            try:
                user = get_object_or_404(User, username=username)
                user_info, created = UserInfo.objects.get_or_create(username=user)  # Đảm bảo UserInfo liên quan đến User
                print(1)

                # Nếu background_image không phải None, xóa hình ảnh cũ và lưu hình ảnh mới
                if background_image:
                    user_info.img_background.delete()
                    user_info.img_background = background_image
                    user_info.img_background_position = scroll_position
                    user_info.save()
                    
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=500)
        else:
            return JsonResponse({'success': False, 'error': 'Người dùng chưa được xác thực'}, status=401)
    else:
        return JsonResponse({'success': False, 'error': 'Phương thức không được phép'}, status=405)

    
def saveAvatar(request):
    if request.method == 'POST':
        username = request.user.username
        avatar_image = request.FILES.get('avatarImage')
        
        try:
            user = User.objects.get(username=username)
            userInfo = UserInfo.objects.get(username=user)
            userInfo.img_avatar.delete()
            userInfo.img_avatar = avatar_image
            userInfo.save()
            return JsonResponse({'success': True})
        except UserInfo.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405) 
