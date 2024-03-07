//tạo nút chuyển qua login và nút chuyển qua register
function toggleModalOpen() {
    $('body').toggleClass('modal-open');
}

function loadRegisterForm() {
    $('#register-form').toggle();
    toggleModalOpen();
}

function closeRegisterForm() {
    $('#register-form').hide();
    toggleModalOpen();
}

function loadLoginForm() {
    $('#login-form').toggle();
    toggleModalOpen();
}

function closeLoginForm() {
    $('#login-form').hide();
    toggleModalOpen();
}

function switchForm() {
    $('#login-form').toggle();
    $('#register-form').toggle();
}


//trả về trang trước
function goBack() {
    window.history.back();
}

