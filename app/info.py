from django.contrib.auth.models import User
from app.models import UserInfo

def username(request):
    info = {}  # Khởi tạo info ngay cả khi không có người dùng xác thực
    if request.user.is_authenticated:
        user = request.user
        try:
            infoUser = UserInfo.objects.get(username=user)
            info['InfoUser'] = infoUser
        except UserInfo.DoesNotExist:
            pass  # Xử lý trường hợp UserInfo không tồn tại cho user đã xác thực
    return info


APP_VERSION = '1.0.0'
APP_NAME = 'AikoNovel'
DEBUG_MODE = False