document.addEventListener('DOMContentLoaded', function() {
    let currentIndex = 0;

    // Функция для получения видимых блоков новостей
    function getVisibleNewsBlock() {
        const newsBlocks = document.querySelectorAll('.news-block');
        for (let block of newsBlocks) {
            if (getComputedStyle(block).display !== 'none') {
                return block; // Возвращаем первый видимый блок
            }
        }
        return null; // Если нет видимых блоков
    }

    // Функция для получения новостей из видимого блока
    function getVisibleNewsItems() {
        const visibleBlock = getVisibleNewsBlock();
        if (visibleBlock) {
            return visibleBlock.querySelectorAll('.news-item');
        }
        return [];
    }

    // Получаем новости из видимого блока
    let visibleNewsItems = getVisibleNewsItems();

    function showNextNews() {
        if (visibleNewsItems.length === 0) return; // Если новостей нет, ничего не делаем

        // Скрываем текущую новость
        visibleNewsItems[currentIndex].style.display = 'none';

        // Переходим к следующей новости
        currentIndex = (currentIndex + 1) % visibleNewsItems.length;

        // Показываем следующую новость
        visibleNewsItems[currentIndex].style.display = 'flex';
    }

    // Устанавливаем интервал для смены новостей каждые 15 секунд
    setInterval(function() {
        // Обновляем список видимых новостей
        visibleNewsItems = getVisibleNewsItems();
        showNextNews();
    }, 15000);
});