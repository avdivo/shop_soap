// Оформление заказа
$(document).ready(function(){

    var fields = {
        'id_last_name': '',
        'id_first_name': '',
        'id_patronymic': '',
        'id_email': '',
        'id_phoneNumber': '',
        'id_address': '',
    }

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

    // Вывести сообщение об оформлении заказа
    $( "#new_order" ).submit(function( event ) {
        $('#exampleModal').modal('show');
    });
    // Запретить закрытие модального окна
     $('#exampleModal').on('hide.bs.modal', function(e) {
           e.preventDefault();
     });

});