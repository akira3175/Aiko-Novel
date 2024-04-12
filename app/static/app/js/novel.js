$(document).ready(function() {
    $('.see-more-chapters').click(function() {
        $(this).hide();
        $(this).parent().css('max-height', 'none');
    });
    $('.volume-list').each(function() {
        var chapterCount = $(this).find('.volume-chapter-details').length;
        if (chapterCount <= 5) {
            $(this).find('.see-more-chapters').hide();
        }
    });
});