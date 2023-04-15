$(document).ready(function () {
    // Обработка кнопки Редактировать
    $("#edit-btn").click(function () {
        $("#name").hide();
        $("#email").hide();
        $(this).hide();
        $("#edit-form").fadeIn();
        $("#close-btn").fadeIn();
    });

    // Обработка кнопки Закрыть
    $("#close-btn").click(function () {
        $("#name").fadeIn();
        $("#email").fadeIn();
        $(this).hide();
        $("#edit-btn").fadeIn();
        $("#edit-form").fadeOut();
    });
});
