function previewImageBackground(event) {
    resetPosition();
    moveBackground();
    var input = event.target;
    var reader = new FileReader();
    reader.onload = function(){
        var dataURL = reader.result;
        var divPreview = document.querySelector('.background-img-overlay');
        var preview = document.querySelector('.background-img-data');
        preview.src = dataURL;
        divPreview.style.backgroundImage = 'url(' + dataURL + ')';
    };
    reader.readAsDataURL(input.files[0]);
    $('.background-img-main').addClass('custom-scrollbar')
    $('.edit-background-container').hide();
    $('.save-edit-background').show();
}

function saveBackgroundImage() {
    var backgroundImage = document.getElementById('background-image-upload').files[0];
    var scrollPosition = document.querySelector('.background-img-main').scrollTop;

    var formData = new FormData();
    formData.append('backgroundImage', backgroundImage);
    formData.append('scrollPosition', scrollPosition);
    console.log(backgroundImage, scrollPosition);

    $.ajax({
        url: '/save-background/', // Địa chỉ URL để xử lý việc lưu trữ vị trí cuộn
        method: 'POST',
        data: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        processData: false,
        contentType: false,
        success: function(response) {
            console.log("Vị trí cuộn của phần tử nền đã được lưu vào cơ sở dữ liệu.");
            location.reload();
        },
        error: function(xhr, status, error) {
            console.error("Đã xảy ra lỗi khi gửi vị trí cuộn của phần tử nền lên máy chủ:", error);
        }
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Kiểm tra xem cookie có bắt đầu bằng tên đã chỉ định không
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function positionBackground() {
    var position = parseInt(document.querySelector('.background-sub').getAttribute('position'));
    document.querySelector('.background-sub').style.top = 'calc(-100% - ' + ( position ) + 'px)';
};

function resetPosition() {
    document.querySelector('.background-sub').style.top = '-100%';
}

document.addEventListener('DOMContentLoaded', function() {
    positionBackground();
    setTopAvatar();
});

function moveBackground() {
    var isMouseDown = false; // Biến để theo dõi xem người dùng có đang giữ chuột không
    var startY = 0;
    var backgroundSub = document.querySelector('.background-img-main');

    document.addEventListener('mousedown', function(event) {
        // Khi người dùng nhấn giữ chuột, đặt biến isMouseDown thành true
        isMouseDown = true;
        startY = event.clientY;
        event.preventDefault();
    });

    document.addEventListener('mouseup', function() {
        // Khi người dùng thả chuột, đặt biến isMouseDown thành false
        isMouseDown = false;
    });

    document.addEventListener('mousemove', function(event) {
        // Khi người dùng di chuyển chuột
        if (isMouseDown) {
            // Nếu người dùng đang giữ chuột, thực hiện cuộn .background-img-main
            var deltaY = event.clientY - startY;
            var direction = deltaY > 0 ? 'down' : 'up';

            // Thực hiện cuộn phần tử tương ứng với hướng di chuyển
            if (direction === 'down') {
                backgroundSub.scrollTop -= Math.abs(deltaY); // Cuộn xuống
            } else {
                backgroundSub.scrollTop += Math.abs(deltaY); // Cuộn lên
            }
            startY = event.clientY; 
        }
    });
}

function setTopAvatar() {
    var navbarHeight = document.querySelector('.navbar').offsetHeight;
    var backgroundImgHeight = document.querySelector('.background-img').offsetHeight;
    var scrollYValue = window.scrollY;
    document.querySelector('.avatar-main-data').style.top = - scrollYValue + navbarHeight + backgroundImgHeight - 60 + 'px';
}

window.addEventListener('scroll', function() {
    setTopAvatar();
});
 
function saveAvatarImage() {
    var avatarImage = document.getElementById('avatar-upload').files[0];
    var formData = new FormData();
    formData.append('avatarImage', avatarImage);

    $.ajax({
        url: '/save-avatar/',
        type: 'POST',
        data: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        processData: false,
        contentType: false,
        success: function(response) {
            console.log("Đã lưu ảnh vào cơ sở dữ liệu.");
            location.reload();
        },
        error: function(xhr, status, error) {
            console.error("Đã xảy ra lỗi khi lưu ảnh lên máy chủ:", error);
        }
    })
}
