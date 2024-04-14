document.addEventListener("DOMContentLoaded", function() {
    var followBtn = document.getElementById("collect");

    followBtn.addEventListener("click", function(e) {
        e.preventDefault(); 
        
        var bookId = this.getAttribute('data-book-id');
        var action = this.getAttribute('data-action');

        var formData = new FormData();
        formData.append('action', action);
        
        fetch(`/follow-book/${bookId}`, {  
            method: "POST",
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                var icon = followBtn.querySelector('i');
                if (action === 'follow') {
                    followBtn.setAttribute('data-action', 'unfollow');
                    icon.style.fontWeight = '900'; 
                } else {
                    followBtn.setAttribute('data-action', 'follow');
                    icon.style.fontWeight = '100'; 
                }
            } else {
                console.error('Follow request failed');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});