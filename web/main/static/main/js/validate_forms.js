function validate_form() {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    let forms = document.querySelectorAll('.needs-validation');

  // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                } else {
                // Если форма валидна, устанавливаем флаг и отправляем форму
                sessionStorage.setItem('formSubmitted', 'true'); // Устанавливаем флаг
            }

            form.classList.add('was-validated');
          }, false)
    });
}


$(function () {
    validate_form();

    // Проверяем флаг из sessionStorage после перезагрузки страницы
    if (sessionStorage.getItem('formSubmitted') === 'true') {
        // Отображаем alert
        $('.alert').css('display', 'flex').delay(3000).fadeOut();

        // Убираем флаг после показа alert
        sessionStorage.removeItem('formSubmitted');
    }
});