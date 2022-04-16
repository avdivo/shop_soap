// Добавление товара в корзину
$(document).ready(function(){
    var form = $('#form_work_basket');

    // Ajax оправление информации об обновлении корзины
    // с заданной задержкой в мс
    var timeOut;
    function sendCanges(change, product, timer){
        if(timeOut)
            clearTimeout(timeOut);
        timeOut = setTimeout(function() {
            var csrf_token = $('#form_work_basket [name="csrfmiddlewaretoken"]').val();
            var url = form.attr("action");
            var data = {
                'change': change,
                'product': product,
                'csrfmiddlewaretoken': csrf_token
            }
            $data = $("#filter_form").serialize();
            $.ajax({
                url: url,
                type: 'POST',
                data: data,
                cache: true,
                success: function (data) {
                    if (change == 'delete'){
                        $('#row_' + product).remove();
                    }
                    updatePage();
                },
                error: function(){
                    console.log(change, product);
                    $('#var-value_' + product).html($('#sum_' + product).html() / $('#price_' + product).html());
                    alert('Ошибка передачи данных!');
                    updatePage();
                }

            });
        }, timer);

    }


    // Отправка формы на странице shop-single.html
    form.on('submit', function(e){
        e.preventDefault(); // Отмена стандартного поведения Submit

        var product_id = $('#product_id').val();
        var quantity = $('#var-value').text();

        update_basket(product_id, quantity)

    });

    // Обработка нажатия кнопок
    // Увеличить/уменьшить количество товаров, отправка формы
    $('.btn').click(function(){
        // Отправка формы
        if ($(this).attr('name') == 'send') {

        }

        // Уменьшить количество товаров
        var var_value = "#var-value_" + $(this).attr('id')
        var value = $(var_value).html()
        if ($(this).attr('name') == 'btn-minus') {
            value = (value=='1')?value:value-1;
        }
        // Увеличить количество товаров
        if ($(this).attr('name') == 'btn-plus') {
            value++;
        }
        $(var_value).html(value);
        var change = 'cange'
        var product = $(this).attr('id')
        var timer = 500
        sendCanges(change, product, timer)


    });


    // Удаление товара из корзины
    $('.manag').on('click', function(e){
        e.preventDefault(); // Отмена стандартного поведения перехода по ссылке
        var change = 'delete';
        var product = $(this).attr('id');
        var timer = 0;
        sendCanges(change, product, timer);
    });


    // Обновление страницы, рассчет сумм
    function updatePage(){
        var all = $(".form-check-input") // Находим все товары по чекбоксам
        var total_sum = 0; // Общая стоимость выделеных товаров
        $.each(all,function(id, obj) {
            var sel_price = '#price_' + obj.name // id цены товара
            var sel_quanity = '#var-value_' + obj.name // id количества товара
            var sel_sum = '#sum_' + obj.name // id суммы товара
            var sum = $(sel_price).html() * $(sel_quanity).html()
            $(sel_sum).html(sum)
            if (obj.checked) {
                total_sum += sum // Включаем в итоговую сумму, если товар выбран
            }
        });
        $('#total_sum').html(total_sum) // Обновляем общую сумму
        if ($(".form-check-input").length == 0) $(".table").remove();
    };


    // Выбрать все товары
    $('#select').on('click', function(e){
        e.preventDefault(); // Отмена стандартного поведения перехода по ссылке
        var all = $(".form-check-input") // Находим все товары по чекбоксам
        $.each(all,function(id, obj) {
            obj.checked = 'checked';
        });
        updatePage();
    });

    // Снять выбор со всех товаров
    $('#clear').on('click', function(e){
        e.preventDefault(); // Отмена стандартного поведения перехода по ссылке
        var all = $(".form-check-input") // Находим все товары по чекбоксам
        $.each(all,function(id, obj) {
            obj.checked = '';
        });
        updatePage();
    });

    // Удалить выбранные товары
    $('#delete').on('click', function(e){
        e.preventDefault(); // Отмена стандартного поведения перехода по ссылке
        var all = $(".form-check-input") // Находим все товары по чекбоксам
        $.each(all,function(id, obj) {
            if (obj.checked) {
                var change = 'delete';
                var product = obj.name;
                var timer = 0;
                sendCanges(change, product, timer);
            }
        });
    });


    // Пересчет сумм при выборе или снятии выбора товаров
    $(".form-check-input").on('change', function(){
        updatePage()
    });

});