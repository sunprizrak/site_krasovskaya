var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
popoverTriggerList.forEach(function (popoverTriggerEl) {
    var trigger = popoverTriggerEl.getAttribute('data-bs-trigger');
    var popover = new bootstrap.Popover(popoverTriggerEl, {
        trigger: trigger
    });
});