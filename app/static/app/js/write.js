document.addEventListener("DOMContentLoaded", function () {
    const chapterContent = document.getElementById("chapter-content");
    const placeholder = document.querySelector(".placeholder-chapter");

    chapterContent.addEventListener("input", function () {
        if (chapterContent.textContent.trim() !== "") {
            placeholder.style.display = "none";
        } else {
            placeholder.style.display = "block";
        }
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
    const content = document.getElementById('chapter-content').innerHTML;
    const chapterId = document.getElementById('writer-editor').getAttribute('chapter-id');
    
    var body = new FormData();
    body.append('content', content);
    body.append('chapter-id', chapterId);
    body.append('csrfmiddlewaretoken', getCookie('csrftoken'));
    console.log(body);

    // Send data using Fetch API
    fetch('/save-chapter/', {  // URL của endpoint Django
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
            console.log('Response from server:', data);
            // Handle server response if needed
        })
        .catch(error => {
            console.error('There was a problem with your fetch operation:', error);
        });
}
