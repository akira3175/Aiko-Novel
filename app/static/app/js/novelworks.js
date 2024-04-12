//Switch types

//dùng để xem người dùng đang ở Main Edit, TOC hay Note
let value = 0;

//Tạo 3 nut chuyển đôỉ qua lại cho chỉnh sửa truyện
const mainEditButton = $('.main-edit-form')
const TOCButton = $('.table-of-contents')
const noteButton = $('.note-works')
const novelId = $('.works-item-metadata').attr('novel-id')

function switchToMainEdit() {
    value = 1;
    mainEditButton.show();
    TOCButton.hide();
    noteButton.hide();
}

function switchToTOC() {
    value = 2;
    mainEditButton.hide();
    TOCButton.show();
    noteButton.hide();
}

function switchToNote() {
    value = 3;
    mainEditButton.hide();
    TOCButton.hide();
    noteButton.show();
}

$('.on-switch-type').click(function() {
    $('.on-switch-type').removeClass('active');
    $(this).addClass('active');
});

$(document).ready(function() {
    if (novelId == 0) {
        switchToMainEdit();
        $('.on-switch-type').eq(0).addClass('active'); 
    } else {
        switchToTOC();
        $('.on-switch-type').eq(1).addClass('active');
    }
});

//Main Edit

function sortCategoryListByValue() {
    var categoryList = document.querySelector('#novel-category .dropdown-menu');
    var categoryItems = categoryList.querySelectorAll('.dropdown-item');

    // Chuyển danh sách NodeList sang mảng để sử dụng các phương thức mảng
    var categoryArray = Array.from(categoryItems);

    // Sắp xếp danh sách theo giá trị của thuộc tính data-value
    categoryArray.sort(function(a, b) {
        var valueA = parseInt(a.getAttribute('data-value'));
        var valueB = parseInt(b.getAttribute('data-value'));
        return valueA - valueB;
    });

    // Xóa tất cả các mục danh mục khỏi danh sách
    categoryList.innerHTML = '';

    // Thêm lại các mục đã sắp xếp vào danh sách
    categoryArray.forEach(function(category) {
        categoryList.appendChild(category);
    });
}

function deleteCategory(element) {
    var category = element.parentElement;
    var categoryName = category.querySelector('.category-name').textContent;
    var categoryId = category.querySelector('.category-name').getAttribute('data-value');
    
    // Tạo một phần tử li mới
    var listItem = document.createElement('li');

    // Tạo phần tử div mới để chứa mục danh mục
    var newCategoryItem = document.createElement('div');
    newCategoryItem.classList.add('dropdown-item');
    newCategoryItem.setAttribute('data-value', categoryId);
    newCategoryItem.textContent = categoryName;

    // Gắn sự kiện xóa danh mục vào phần tử mới
    newCategoryItem.onclick = function() {
        removeCategory(this);
    };

    // Gắn phần tử div vào phần tử li
    listItem.appendChild(newCategoryItem);

    // Tìm và thêm phần tử li vào danh sách mục
    var categoryList = document.querySelector('#novel-category .dropdown-menu');
    categoryList.appendChild(listItem);

    //Sắp xếp danh sách
    sortCategoryListByValue();

    // Xóa phần tử danh mục khỏi giao diện người dùng
    category.remove();
}


document.addEventListener('DOMContentLoaded', function() {

    //Tạo thẻ button cho thể loại khi chọn trong danh sách thể loại
    var dropdownMenu = document.getElementById('dropdown-menu');
    var novelCategory = document.getElementById('novel-category');

    dropdownMenu.addEventListener('click', function(event) {
        if (event.target.classList.contains('dropdown-item')) {
            var selectedCategory = event.target.textContent;
            var selectedCategoryValue = event.target.getAttribute('data-value');
            addCategory(selectedCategory, selectedCategoryValue);
            updateCategorySearchPosition();
        }
    });

    function addCategory(category, categoryValue) {
        var categoryDiv = document.createElement('div');
        categoryDiv.classList.add('category-button');

        var categoryName = document.createElement('div');
        categoryName.textContent = category;
        categoryName.setAttribute('data-value', categoryValue);
        categoryName.classList.add('category-name');
        
        var lineDiv = document.createElement('div');
        lineDiv.classList.add('line');

        var cancelDiv = document.createElement('div');
        cancelDiv.classList.add('category-cancel');

        var cancelIcon = document.createElement('i');
        cancelIcon.classList.add('fa-solid', 'fa-xmark');
        cancelDiv.appendChild(cancelIcon);

        cancelDiv.setAttribute('onclick', 'deleteCategory(this);');

        categoryDiv.appendChild(categoryName);
        categoryDiv.appendChild(lineDiv);
        categoryDiv.appendChild(cancelDiv);
        categoryDiv.setAttribute('contenteditable', 'false');
        
        novelCategory.appendChild(categoryDiv);
    }

});

var novelCategory = document.querySelector('.novel-category');
var dropdownMenu = document.querySelector('.dropdown-menu');

function toggleDropdown() {
    var dropdownMenu = document.getElementById('dropdown-menu');
    dropdownMenu.classList.toggle('show');
}

//tắt dropdown khi nhấp ngoài ô thể loại
window.onclick = function(event) {
    var dropdownMenu = document.getElementById('dropdown-menu');
    var novelCategory = document.getElementById('novel-category');

    if (!novelCategory.contains(event.target)) {
        dropdownMenu.classList.remove('show');
    }
}


var novelCategory = document.getElementById('novel-category');
var categorySearch = document.querySelector('.category-search');

//đảm bảo ô input luôn nằm sau cùng các thẻ thể loại khác
function updateCategorySearchPosition() {
    novelCategory.appendChild(categorySearch);
}

//tự động trỏ chuột vào ô input khi nhấp vào ô thể loại

novelCategory.addEventListener('click', function() {
    categorySearch.focus();
});

$(document).ready(function() {
    $('input').on('input', function() {
        $(this).css('width', $(this).val().length * 9 + 'px'); // chỉnh độ dài cho ô tìm kiểm thể loại
    });
});

function removeCategory(item) {
    item.remove();
}


//Cho người dùng xem trước ảnh
function previewImage(event) {
    console.log(value);
    var input = event.target;
    var reader = new FileReader();
    var preview;
    console.log(value == 1)
    if (value == "1") {
        preview = document.querySelector('.preview');
    }
    else if (value == "2") {
        preview = document.querySelector('.preview-volume');
    }
    reader.onload = function(){
        var dataURL = reader.result;
        preview.src = dataURL;
        
    };
    reader.readAsDataURL(input.files[0]);
}

function getValueForCategory() {
    // Lấy tất cả các phần tử có lớp là "category-name"
    const categoryElements = document.querySelectorAll('.category-name');
    // Mảng để lưu trữ các giá trị data-value
    const dataValues = [];
    // Lặp qua từng phần tử và trích xuất giá trị data-value
    categoryElements.forEach(function(element) {
        const dataValue = element.getAttribute('data-value');
        dataValues.push(dataValue);
    });
    // Chuyển mảng thành chuỗi bằng cách sử dụng phương thức join
    const dataValuesString = dataValues.join(',');
    // In ra chuỗi các giá trị data-value
    console.log(dataValuesString);
    return dataValuesString;
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

function saveBook() {
    var novelid = document.querySelector('.works-item-metadata').getAttribute('novel-id');
    var title = document.querySelector('.novel-title').innerText;
    var author = document.querySelector('.novel-author').innerText;
    var artist = document.querySelector('.novel-artist').innerText;
    var novelTransTeam = document.querySelector('.novel-trans-team').getAttribute('worker-id');
    var category = getValueForCategory();
    var description = document.querySelector('.novel-description').value;
    var checkboxChecked = document.querySelector('.novel-status input[type="checkbox"]').checked;
    var file = document.getElementById('image-upload').files[0];

    var formData = new FormData();
    formData.append('novelid', novelid);
    formData.append('title', title);
    formData.append('author', author);
    formData.append('artist', artist);
    formData.append('novelTransTeam', novelTransTeam);
    formData.append('category', category);
    formData.append('description', description);
    formData.append('checkboxChecked', checkboxChecked);
    formData.append('image', file);

    fetch('/saveBook', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url; // Chuyển hướng trình duyệt
        }
        return response.json(); // Phân tích dữ liệu JSON nếu cần thiết
    })
    .then(data => {
        console.log(data);
        // Xử lý phản hồi từ máy chủ nếu cần thiết
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

//Table of Contents
function openAddVolumeForm(event, value) {
    event.preventDefault();
    let text = "";
    let textButton = "";
    if (value == 0) {
        text = "Thêm tập mới";
        textButton = "Thêm tập";
    }
    else {
        text = "Sửa tập";
        textButton = "Sửa tập";
        var volumeContainer = event.target.closest('.works-item-volume');
        var volumeName = volumeContainer.querySelector('.volume-name').textContent.trim();
        var volumeImage = volumeContainer.querySelector('.volume-img-main').getAttribute('src');
        document.getElementById('volume-name').value = volumeName;
        document.querySelector('.preview-volume').setAttribute('src',volumeImage);
    }
    $('.form-title').text(text);
    $('#add-volume-form .el-button').text(textButton);
    console.log(2);
    $('#add-volume-form').attr('volume-id', value);
    $("#add-volume-form").toggle();
    toggleModalOpen();
}

function closeAddVolumeForm() {
    $("#add-volume-form").toggle();
    toggleModalOpen();
}

function saveVolume() {
    var bookId = document.getElementById('novel-id').getAttribute('novel-id');
    var volumeId = document.getElementById('add-volume-form').getAttribute('volume-id');
    var volumeImage = document.getElementById('volume-image-upload').files[0];
    var title = document.getElementById('volume-name').value;

    var formData = new FormData();
    formData.append('book-id', bookId);
    formData.append('volume-id', volumeId);
    formData.append('volume-image', volumeImage);
    formData.append('volume-title', title);
    console.log(bookId);

    $.ajax({
        url: '/save-volume/', 
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        data: formData,
        contentType: false,
        processData: false,
        success: function(response) {
            console.log(2);
        },
        error: function(xhr, status, error) {
            alert('Đã xảy ra lỗi khi lưu tập!');
        }
    });    
}

$(document).ready(function() {
    $('.see-more-chapters').click(function() {
        $(this).hide();
        $(this).parent().css('max-height', 'none');
    });
    // Kiểm tra số lượng chương của mỗi tập và ẩn hiện class show-more-chapters
    $('.works-item-volume').each(function() {
        var chapterCount = $(this).find('.volume-chapter-details').length;
        if (chapterCount <= 6) {
            $(this).find('.see-more-chapters').hide(); // Ẩn nút "Xem thêm chương"
        }
    });
});



//Note
