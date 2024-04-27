/*Login*/

document.querySelector('#login-form #username').addEventListener('blur', function() {
    validateUsernameLogin();
});

var isValidUsernameLogin = false;
var isValidPasswordLogin = false;


function validateUsernameLogin() {
    var usernameInput = document.querySelector('#login-form #username');
    var username = usernameInput.value.trim();
    var usernameContainer = usernameInput.parentElement;
    var usernameError = document.querySelector('#login-form #username-error');
    var usernameLabel = usernameContainer.querySelector('.el-input-inner');

    if (username === '') {
        usernameError.innerText = 'Tài khoản không được để trống';
        usernameError.style.display = 'block';
        usernameContainer.classList.add('error');
        usernameLabel.classList.add('error');
        isValidUsernameLogin = false;
    } else {
        usernameError.style.display = 'none';
        usernameContainer.classList.remove('error');
        usernameLabel.classList.remove('error');
        isValidUsernameLogin = true; 
    }
}

document.querySelector('#login-form #password').addEventListener('blur', function() {
    validatePasswordLogin();
});

function validatePasswordLogin() {
    var passwordInput = document.querySelector('#login-form #password');
    var password = passwordInput.value.trim();
    var passwordContainer = passwordInput.parentElement;
    var passwordError = document.querySelector('#login-form #password-error');
    var passwordLabel = passwordContainer.querySelector('.el-input-inner');

    if (password === '') {
        passwordError.innerText = 'Mật khẩu không được để trống';
        passwordError.style.display = 'block';
        passwordContainer.classList.add('error');
        passwordLabel.classList.add('error'); 
        isValidPasswordLogin = false; 
    } else {
        passwordError.style.display = 'none';
        passwordContainer.classList.remove('error');
        passwordLabel.classList.remove('error');
        isValidPasswordLogin = true; 
    }
}

function toggleLoginButton() {
    var loginButton = document.querySelector('#login-form .el-button');
    var username = document.querySelector('#login-form #username').value.trim();
    var password = document.querySelector('#login-form #password').value.trim();

    if (username === '' || password === '') {
        loginButton.classList.add('disable');
        loginButton.disabled = true;
    } else {
        loginButton.classList.remove('disable');
        loginButton.disabled = false;
    }
}

document.querySelector('#login-form #username').addEventListener('input', toggleLoginButton);
document.querySelector('#login-form #password').addEventListener('input', toggleLoginButton);

/* Register */

var typingTimerUsername;
var typingTimerEmail;
var typingTimerPassword;
var typingTimerRepassword;
var doneTypingInterval = 1000;

var isValidUsernameRegister = false;
var isValidEmailRegister = false;
var isValidPasswordRegister = false;
var isValidRepasswordRegister = false;
var isAgreeToTerms = false;

function showError(element, elementText) {
    var elementContainer = element.parentElement;
    var elementError = elementContainer.parentElement.querySelector('.error-text');
    var elementLabel = elementContainer.querySelector('.el-input-inner');

    if (elementText === '') {
        elementError.style.display = 'none';
        elementContainer.classList.remove('error');
        elementLabel.classList.remove('error');
    }
    else {
        elementError.innerText = elementText;
        elementError.style.display = 'block';
        elementContainer.classList.add('error');
        elementLabel.classList.add('error');
    }
}

$('#register-form #username').on('input', function(){
    clearTimeout(typingTimerUsername);
    typingTimerUsername = setTimeout(checkUsernameRegister, doneTypingInterval);
});

function checkUsernameRegister() {
    var usernameInput = document.querySelector('#register-form #username');
    var username = usernameInput.value.trim();
    var error = '';

    if (username === '') {
        error = 'Tên người dùng không được để trống!';
        isValidUsernameRegister = false;
        showError(usernameInput, error);
        toggleRegisterButton();
    } else if (!checkUsernameLength(username)) {
        error = 'Tên người dùng phải có từ 8 đến 32 ký tự!';
        isValidUsernameRegister = false;
        showError(usernameInput, error);
        toggleRegisterButton();
    } else {
        $.ajax({
            url: '/check-username/',
            data: {
                'username': username
            },
            dataType: 'json',
            success: function(data) {
                if (!data.is_taken) {
                    error = '';
                    isValidUsernameRegister = true;
                } else {
                    error = 'Tên người dùng đã tồn tại!';
                    isValidUsernameRegister = false;
                }
                showError(usernameInput, error);
                toggleRegisterButton();
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error("AJAX request failed:", textStatus, errorThrown);
            }
        });
    }
}



// Kiểm tra username dài từ 8-16 ký tự
function checkUsernameLength(username) {
    if (username.length < 8 || username.length > 32) {
        return false;
    } else {
        return true;
    }
}

$('#register-form #email').on('input', function(){
    clearTimeout(typingTimerEmail);
    typingTimerEmail = setTimeout(checkEmailRegister, doneTypingInterval);
});

function checkEmailRegister() {
    var emailInput = document.querySelector('#register-form #email');
    var email = emailInput.value.trim();
    var error = '';

    if (email === '') {
        error = 'Email không được để trống!';
        isValidEmailRegister = false;
        showError(emailInput, error);
        toggleRegisterButton(); 
    } else if (!isValidEmail(email)) {
        error = 'Email không hợp lệ!';
        isValidEmailRegister = false;
        showError(emailInput, error);
        toggleRegisterButton(); 
    } else {
        $.ajax({
            url: '/check-email/',  
            data: {
                'email': email
            },
            dataType: 'json'
        }).done(function(data) {
            if (!data.is_taken) {
                error = '';
                isValidEmailRegister = true;
            } else {
                error = 'Email đã tồn tại!';
                isValidEmailRegister = false;
            }
            showError(emailInput, error);
            toggleRegisterButton(); 
        }).fail(function(jqXHR, textStatus, errorThrown) {
            console.error("AJAX request failed:", textStatus, errorThrown);
        });
    }
}

function isValidEmail(email) {
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

$('#register-form #password').on('input', function(){
    clearTimeout(typingTimerPassword);
    typingTimerPassword = setTimeout(checkPasswordRegister, doneTypingInterval);
});

var checked = false;

function checkPasswordRegister() {
    var passwordInput = document.querySelector('#register-form #password');
    var password = passwordInput.value.trim();
    var repasswordInput = document.querySelector('#register-form #repassword');
    var repassword = repasswordInput.value.trim();
    var error = '';

    if (!checkPasswordLength(password)) {
        error = 'Mật khẩu phải có từ 8 đến 32 ký tự!';
        isValidPasswordRegister = false;
    } else if (!isValidPassword(password)) {
        error = 'Mật khẩu phải chứa ít nhất một chữ cái và một chữ số!';
        isValidPasswordRegister = false;
    } else {
        error = '';
        isValidPasswordRegister = true;
    }
    showError(passwordInput, error);
    if (repassword !== '' && checked == false) {
        checked = true;
        checkRepasswordRegister();
    }
    checked = false;
    toggleRegisterButton();
}

function checkPasswordLength(password) {
    return password.length >= 8 && password.length <= 32;
}

function isValidPassword(password) {
    var hasLetter = /[a-zA-Z]/.test(password);
    var hasDigit = /\d/.test(password);
    return hasLetter && hasDigit;
}

$('#register-form #repassword').on('input', function(){
    clearTimeout(typingTimerRepassword);
    typingTimerRepassword = setTimeout(checkRepasswordRegister, doneTypingInterval);
});

function checkRepasswordRegister() {
    var repasswordInput = document.querySelector('#register-form #repassword');
    var repassword = repasswordInput.value.trim();
    var passwordInput = document.querySelector('#register-form #password');
    var password = passwordInput.value.trim();
    var error = '';

    if (password !== repassword) {
        error = 'Mật khẩu nhập lại không khớp!';
        isValidRepasswordRegister = false;
    } else {
        error = '';
        isValidRepasswordRegister = true;
    }
    showError(repasswordInput, error);
    if (checked == false) {
        check = true;
        checkPasswordRegister();
    }
    checked = false;
    toggleRegisterButton();
}

function toggleCheckAggreToTerms() {
    isAgreeToTerms = !isAgreeToTerms;
    toggleRegisterButton();
}

function toggleRegisterButton() {
    var registerButton = document.querySelector('#register-form .el-button');

    if (meetTheRequirements()) {
        registerButton.classList.remove('disable');
        registerButton.disabled = false;
    } else {
        registerButton.classList.add('disable');
        registerButton.disabled = true;
    }
}

function meetTheRequirements() {
    return isValidUsernameRegister && isValidEmailRegister && isValidPasswordRegister && isValidRepasswordRegister && isAgreeToTerms;
}

document.addEventListener('DOMContentLoaded', function() {
    var registerButton = document.querySelector('#register-form .el-button');
    var loginButton = document.querySelector('#login-form .el-button');

    registerButton.disabled = true;
    loginButton.disabled = true;
});