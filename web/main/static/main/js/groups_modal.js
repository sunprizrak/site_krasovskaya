// Функция для установки значения группы при открытии модального окна
 $(document).ready(function() {
    // Когда модальное окно открывается
    $('#groups-modal').on('show.bs.modal', function () {
        // Получаем активный элемент карусели
        var activeItem = $('#groups-middle .carousel-item.active');
        // Получаем id группы из атрибута data-group-id
        var groupId = activeItem.data('group-id');

        // Устанавливаем значение groupId в поле select в форме
        $('#id_group').val(groupId);
    });
});