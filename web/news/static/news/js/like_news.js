$(document).ready(function() {
    $('.heart-stat').click(function() {
        var newsId = $(this).data('news-id');
        var likeCount = $(this).find('span');

        $.ajax({
            url: NewsUrl,
            type: 'POST',
            data: {
                'news_id': newsId,
                'csrfmiddlewaretoken': csrfToken,
            },
            success: function(data) {
                if (data.success) {
                    likeCount.text(data.likes);
                }
            }.bind(this)
        });
    });
});