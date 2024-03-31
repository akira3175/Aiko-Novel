function showShare(){
    var share = document.getElementById('sharing-box');
    if (share !== null) {
        if (share.style.display === 'none' || share.style.display === '') {
            share.style.display = 'block';
        } else {
            share.style.display = 'none';
        }
    } else {
        console.error("Element with ID 'sharing-box' not found.");
    }
}