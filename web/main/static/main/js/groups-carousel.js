function applyFadeOnMd() {
    const carousel = document.getElementById('groups-carousel');
    if (window.innerWidth >= 768) {
        carousel.classList.add('carousel-fade');
    } else {
        carousel.classList.remove('carousel-fade');
    }
}

// Запуск при загрузке страницы и при изменении размера окна
applyFadeOnMd();
window.addEventListener('resize', applyFadeOnMd);