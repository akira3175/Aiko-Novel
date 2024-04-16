from django.contrib.auth.models import User
from app.models import UserInfo

def get_user_info(request):
    info = {}  # Khởi tạo info ngay cả khi không có người dùng xác thực
    if request.user.is_authenticated:
        user = request.user
        try:
            info_user = UserInfo.objects.get(username=user)
            info['InfoUser'] = info_user
            print(info['InfoUser'].img_avatar)  # Di chuyển việc truy cập thuộc tính vào trong khối try
        except UserInfo.DoesNotExist:
            info['error'] = "Thông tin người dùng không tồn tại."
    return info



APP_VERSION = '1.0.0'
APP_NAME = 'AikoNovel'
DEBUG_MODE = False