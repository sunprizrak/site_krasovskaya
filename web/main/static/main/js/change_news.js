document.addEventListener('DOMContentLoaded', function() {
    let currentIndex = 0;
    const newsItems = document.querySelectorAll('.news-item');

    function showNextNews() {
        // Скрываем текущую новость
        newsItems[currentIndex].style.display = 'none';

        // Переходим к следующей новости
        currentIndex = (currentIndex + 1) % newsItems.length;

        // Показываем следующую новость
        newsItems[currentIndex].style.display = 'block';
    }

    // Устанавливаем интервал для смены новостей каждые 15 секунд
    setInterval(showNextNews, 15000);
});