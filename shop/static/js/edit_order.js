// Оформление заказа
$(document).ready(function(){


// Отправка формы при выборе select
$('#select_status').on('change', function() {
  $(this.form).submit();
});

// Выбор шаблона
$('.sam').on('click', function() {
//console.log($(this).text())

    var $txt = jQuery("#message");
    var caretPos = $txt[0].selectionStart;
    var textAreaTxt = $txt.val();
    var txtToAdd = $(this).text();
    $txt.val(textAreaTxt.substring(0, caretPos) + txtToAdd + textAreaTxt.substring(caretPos) );

});



});