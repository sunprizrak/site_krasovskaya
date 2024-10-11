document.addEventListener('DOMContentLoaded', function () {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));

    const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        const popover = new bootstrap.Popover(popoverTriggerEl, {
            trigger: 'manual',
            html: true
        });

        let popoverTimeout;

        // Показываем поповер при наведении на элемент
        popoverTriggerEl.addEventListener('mouseenter', function () {
            popover.show();
            clearTimeout(popoverTimeout);

            // Обработчик события для поповера
            const popoverEl = document.querySelector('.popover');

            if (popoverEl) {
                popoverEl.addEventListener('mouseenter', function () {
                    clearTimeout(popoverTimeout); // Останавливаем таймер для скрытия поповера
                });

                popoverEl.addEventListener('mouseleave', function () {
                    popoverTimeout = setTimeout(function () {
                        popover.hide(); // Скрываем поповер с задержкой
                    }, 200);
                });
            }
        });

        // Скрываем поповер при уходе с элемента
        popoverTriggerEl.addEventListener('mouseleave', function () {
            popoverTimeout = setTimeout(function () {
                const popoverEl = document.querySelector('.popover:hover');
                if (!popoverEl) {
                    popover.hide();
                }
            }, 200); // Даем небольшую задержку перед скрытием
        });
    });
});