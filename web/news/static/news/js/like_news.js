$(document).ready(function() {
    $('.heart').click(function() {
        var newsId = $(this).data('news-id');
        var likeCount = $(this).find('span');

        $.ajax({
            url: '',
            type: 'POST',
            data: {
                'news_id': newsId,
                'csrfmiddlewaretoken': csrfToken,
            },
            success: function(data) {
                if (data.success) {
                    likeCount.text(data.likes);
                } else {
                    alert(data.message);
                }
            }
        });
    });
});