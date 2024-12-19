function applyFadeOnMd() {
    const carousels = document.querySelectorAll('.groups-carousel');
    carousels.forEach(carousel => {
        if (window.innerWidth >= 999) {
            carousel.classList.add('carousel-fade');
        } else {
            carousel.classList.remove('carousel-fade');
        }
    });
}

// Запуск при загрузке страницы и при изменении размера окна
applyFadeOnMd();
window.addEventListener('resize', applyFadeOnMd);



$(document).ready(function () {
    // Получаем ссылки на элементы форм
    const constantForm = $('#groups-box-form-constant');
    const onTimeForm = $('#groups-box-form-on_time_lessons');

    // Получаем ссылки на элементы полей выбора групп
    const constantGroupField = $('.select-col').find('[name="constant_group"]').parent();
    const onTimeGroupField = $('.select-col').find('[name="on_time_group"]').parent();


    // Функция для отображения формы постоянных групп
    function showConstantForm() {
        constantForm.show();  // Показываем форму постоянных групп
        onTimeForm.hide();    // Скрываем форму разовых мероприятий
        constantGroupField.show(); // Показываем поле постоянных групп
        onTimeGroupField.hide();   // Скрываем поле разовых групп
        // Устанавливаем поле constant_group как обязательное
        $('#id_constant_group').prop('required', true);
        // Убираем обязательность для on_time_group
        $('#id_on_time_group').prop('required', false);
    }

    // Функция для отображения формы разовых мероприятий
    function showOnTimeForm() {
        constantForm.hide();  // Скрываем форму постоянных групп
        onTimeForm.show();    // Показываем форму разовых мероприятий
        constantGroupField.hide(); // Скрываем поле постоянных групп
        onTimeGroupField.show();   // Показываем поле разовых групп
        $('#id_on_time_group').prop('required', true);
        // Убираем обязательность для constant_group
        $('#id_constant_group').prop('required', false);
    }

    // Назначаем обработчики событий для вкладок
    $('#groups-button-tabs-left').on('click', showConstantForm);
    $('#groups-button-tabs-right').on('click', showOnTimeForm);

    // Инициализация: показываем форму для активной вкладки
    if ($('#groups-button-tabs-left').hasClass('active')) {
        showConstantForm();
    } else {
        showOnTimeForm();
    }

    // Обработка переключения карусели
    $('.carousel-button svg').on('click', function () {
        $(this).addClass('clicked');
        setTimeout(() => {
            $(this).removeClass('clicked');
        }, 1000);
    });

    function getActiveCarousel() {
        if ($('#groups-button-tabs-left').hasClass('active')) {
            return $('#groups-carousel-constant');
        }
        if ($('#groups-button-tabs-right').hasClass('active')) {
            return $('#groups-carousel-on_time_lessons');
        }
        return null;
    }

    $('#custom-carousel-prev svg').on('click', function () {
        const activeCarousel = getActiveCarousel();
        if (activeCarousel) {
            activeCarousel.carousel('prev'); // Переключение на предыдущий слайд
        }
    });

    $('#custom-carousel-next svg').on('click', function () {
        const activeCarousel = getActiveCarousel();
        if (activeCarousel) {
            activeCarousel.carousel('next'); // Переключение на следующий слайд
        }
    });
});