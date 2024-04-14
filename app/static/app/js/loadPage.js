//tạo nút chuyển qua login và nút chuyển qua register
function toggleModalOpen() {
  $("body").toggleClass("modal-open");
}

function loadRegisterForm() {
  $("#register-form").toggle();
  toggleModalOpen();
}

function closeRegisterForm() {
  $("#register-form").hide();
  toggleModalOpen();
}

function loadLoginForm() {
  $("#login-form").toggle();
  toggleModalOpen();
}

function closeLoginForm() {
  $("#login-form").hide();
  toggleModalOpen();
}

function loadAddGroupForm() {
  $("#addgroup-form").toggle();
  toggleModalOpen();
}

function closeAddGroupForm() {
  $("#addgroup-form").hide();
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

window.addEventListener('scroll', function() {
    var scrollPosition = window.scrollY;
    var parallaxElements = document.querySelectorAll('.parallax-section');

    parallaxElements.forEach(function(element) {
        var speed = parseFloat(element.dataset.speed);
        var translateY = -scrollPosition * speed;
        element.style.transform = 'translateY(' + translateY + 'px)';
    });
});

$(document).ready(function() {
  var navbar = $('.navbar');
  var lastScrollTop = 0;

  $(window).scroll(function() {
    var currentScroll = $(this).scrollTop();
    if (currentScroll < lastScrollTop) {
      // Cuộn xuống
      navbar.addClass('sticky-top');
    } else {
      // Cuộn lên
      navbar.removeClass('sticky-top');
    }
    lastScrollTop = currentScroll <= 0 ? 0 : currentScroll; // Đảm bảo lastScrollTop không âm
  });

  $(window).on('load resize', function() {
    if ($(window).width() < 992) {
      var searchForm = $('#search-form');
      searchForm.prependTo(searchForm.parent());
    }
    else {
      var searchForm = $('#search-form');
      searchForm.insertAfter(searchForm.siblings().eq(0));
    }
  });
});
