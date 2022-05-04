// Оформление заказа
$(document).ready(function(){


// Запоминаем поля формы при загрузке страницы
$.each(fields, function(sel, i) {
    fields[sel] = $('#' + sel).val();
});


// Включить или выключить редактирование полей формы переключателем
$(".form-check-input").on('change', function(){
     if ($(this).prop('checked')){
         $.each(fields, function(sel, i) {
            $('#' + sel).prop('readonly', true);
            $('#' + sel).val(fields[sel]);
         });
     } else {
         $.each(fields, function(sel, i) {
            $('#' + sel).prop('readonly', false);
         });
     }

});



});