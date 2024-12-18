$(document).ready(function () {
    $(".groups-item-body-fullscreen").click(function () {
        var target = $(this).data("target");
        console.log(target);
        var activeItem = $('.carousel-item.active');

        // Добавляем/удаляем класс
        $(target).toggleClass("fullscreen");
        activeItem.toggleClass("fullscreen");
    });
});