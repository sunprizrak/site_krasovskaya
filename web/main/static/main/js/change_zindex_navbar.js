document.addEventListener('DOMContentLoaded', function() {
    const navbarCollapse = document.getElementById('navbarNavAltMarkup');
    const header = document.querySelector('header');

    // Событие при открытии меню
    navbarCollapse.addEventListener('show.bs.collapse', function () {
        header.style.zIndex = '1000'; // Меняем z-index хедера при открытии меню
    });

    // Событие при закрытии меню
    navbarCollapse.addEventListener('hidden.bs.collapse', function () {
        header.style.zIndex = '10'; // Возвращаем z-index хедера после закрытия меню
    });
});