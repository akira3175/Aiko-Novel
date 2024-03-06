//Switch types

const mainEditButton = $('.main-edit-form')
const TOCButton = $('.table-of-contents')
const noteButton = $('.note-works')

function switchToMainEdit() {
    mainEditButton.show();
    TOCButton.hide();
    noteButton.hide();
}

function switchToTOC() {
    mainEditButton.hide();
    TOCButton.show();
    noteButton.hide();
}

function switchToNote() {
    mainEditButton.hide();
    TOCButton.hide();
    noteButton.show();
}

$('.on-switch-type').click(function() {
    $('.on-switch-type').removeClass('active');
    $(this).addClass('active');
});

//Main Edit

function deleteCategory(element) {
    element.parentElement.remove();
}

document.addEventListener('DOMContentLoaded', function() {
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

window.onclick = function(event) {
    var dropdownMenu = document.getElementById('dropdown-menu');
    var novelCategory = document.getElementById('novel-category');

    if (!novelCategory.contains(event.target)) {
        dropdownMenu.classList.remove('show');
    }
}

function updateCategorySearchPosition() {
    var novelCategory = document.getElementById('novel-category');
    var categorySearch = document.querySelector('.category-search');
    novelCategory.appendChild(categorySearch);
}

var novelCategory = document.getElementById('novel-category');
var categorySearch = document.querySelector('.category-search');

novelCategory.addEventListener('click', function() {
    categorySearch.focus();
});

//Table of Contents

//Note
