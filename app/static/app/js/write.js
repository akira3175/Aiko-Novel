document.addEventListener("DOMContentLoaded", function () {
    const chapterContent = document.getElementById("chapter-content");
    const placeholder = document.querySelector(".placeholder-chapter");

    function togglePlaceholder() {
        if (chapterContent.textContent.trim() !== "") {
            placeholder.style.display = "none";
        } else {
            placeholder.style.display = "block";
        }
    }

    togglePlaceholder();

    chapterContent.addEventListener("input", togglePlaceholder);
    chapterContent.addEventListener("paste", function () {
        setTimeout(function () {
            togglePlaceholder();
        }, 1);
    });
});
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

function saveChapter() {
    const title = document.getElementById('chapter-title-input').value;
    const content = document.getElementById('chapter-content').innerHTML;
    const chapterId = document.getElementById('writer-editor').getAttribute('chapter-id');
    const novelId = document.querySelector('.works-item-metadata').getAttribute('novel-id');

    var body = new FormData();
    body.append('title', title);
    body.append('content', content);
    body.append('chapter-id', chapterId);
    body.append('novel-id', novelId);
    body.append('csrfmiddlewaretoken', getCookie('csrftoken'));

    // Send data using Fetch API
    fetch('/save-chapter/', {
        method: 'POST',
        body: body,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.redirect_url) {
            window.location.href = data.redirect_url; // Thực hiện redirect từ client
        } else {
            console.error('Redirect URL not found in server response');
        }
    })
    .catch(error => {
        console.error('There was a problem with your fetch operation:', error);
    });
}

function uploadChapter() {
    const title = document.getElementById('chapter-title-input').value;
    const content = document.getElementById('chapter-content').innerHTML;
    const chapterId = document.getElementById('writer-editor').getAttribute('chapter-id');
    const novelId = document.querySelector('.works-item-metadata').getAttribute('novel-id');

    var body = new FormData();
    body.append('title', title);
    body.append('content', content);
    body.append('chapter-id', chapterId);
    body.append('novel-id', novelId);
    body.append('csrfmiddlewaretoken', getCookie('csrftoken'));

    // Send data using Fetch API
    fetch('/upload-chapter/', {
        method: 'POST',
        body: body,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.redirect_url) {
            window.location.href = data.redirect_url; // Thực hiện redirect từ client
        } else {
            console.error('Redirect URL not found in server response');
        }
    })
    .catch(error => {
        console.error('There was a problem with your fetch operation:', error);
    });
}

function deleteChapter() {
    const chapterId = document.getElementById('writer-editor').getAttribute('chapter-id');
    const novelId = document.querySelector('.works-item-metadata').getAttribute('novel-id');

    var body = new FormData();
    body.append('chapter-id', chapterId);
    body.append('novel-id', novelId);
    body.append('csrfmiddlewaretoken', getCookie('csrftoken'));

    // Send data using Fetch API
    fetch('/delete-chapter/', {
        method: 'POST',
        body: body,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.redirect_url) {
            window.location.href = data.redirect_url; // Thực hiện redirect từ client
        } else {
            console.error('Redirect URL not found in server response');
        }
    })
    .catch(error => {
        console.error('There was a problem with your fetch operation:', error);
    });
}