
//khi load page luôn mở cái ô đầu tiên

document.addEventListener("DOMContentLoaded", function() {
    var worksTypeButton = document.querySelector('#content-works .works-type-select button');
    worksTypeButton.classList.add('active');
});

