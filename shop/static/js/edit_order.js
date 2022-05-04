// Оформление заказа
$(document).ready(function(){


    // Отправка формы при выборе select
    $('#select_status').on('change', function() {
      $(this.form).submit();
    });

    // Выбор шаблона. Отправляем форму с новым статусом
    $('.sam').on('click', function() {

        var $txt = jQuery("#message");
        var caretPos = $txt[0].selectionStart;
        var textAreaTxt = $txt.val();
        var txtToAdd = $(this).text();
        $txt.val(textAreaTxt.substring(0, caretPos) + txtToAdd + textAreaTxt.substring(caretPos));

    });

    // Очистка письма и поля для ввода
    $('#clear').on('click', function() {
        $("#message").val('')
        $("#insert").html('')
    });

    // Вставка текста из поля в письмо
    $('#add').on('click', function() {
        // console.log($("#message").val())
        var arr = $("#message").val().split('\n'); // Разбивка содержимого по переносу строки
        var str = '';
        $.each(arr,function(index,value){
            // Оборачиваем каждую подстроку в тег <p></p>
            str += '<p>' + value + '</p>';
        });
        $("#insert").html(str);
    });

});