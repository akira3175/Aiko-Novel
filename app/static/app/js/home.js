$(document).ready(function () {
    $("#slider").owlCarousel({
        items: 4, // Số item hiển thị trên PC
        margin: 10,
        autoplay: true,
        autoplayTimeout: 3000,
        autoplayHoverPause: true,
        responsive: {
            0: {
                items: 2 // Số item hiển thị trên điện thoại di động
            },
            768: {
                items: 3 // Số item hiển thị trên tablet
            },
            1024: {
                items: 4 // Số item hiển thị trên PC và màn hình lớn hơn
            }
        }
    });
});