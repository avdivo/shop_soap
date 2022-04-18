// Добавление товара в корзину
$(document).ready(function(){
    var form = $('#form_work_basket');
    updatePage();

    // Ajax оправление информации об обновлении корзины
    // с заданной задержкой в мс
    var timeOut;
    function sendCanges(data, change, product, timer){
        if(timeOut)
            clearTimeout(timeOut);
        timeOut = setTimeout(function() {
            var csrf_token = $('#form_work_basket [name="csrfmiddlewaretoken"]').val();
            var url = form.attr("action");
            data['csrfmiddlewaretoken'] = csrf_token
            console.log(data);
            $.ajax({
                url: url,
                type: 'POST',
                data: data,
                cache: true,
                success: function (data) {
                    // Операция успешно выполнена
                    if (change == 'delete'){
                        // Удаляем кандидатов на удаление (на сервере это уже сделано)
                        $.each(product, function(i, del) {
                            $('#row_' + del).remove();
                        });
                    }
                    // Изменяем отображаемое значение на корзине
                    b = (data.products == 0) ? '' : data.products;
                    $('#quantity_in_basket').text(b);
                    updatePage();
                },
                error: function(){
                    console.log('error');
                    // Произошла ошибка связи с сервером или обновления данных
                    if (change == 'change') {
                        // Отменяем добавление или отнятие товаров в корзину
                        $('#var-value_' + product).html($('#sum_' + product).html() / $('#price_' + product).html());
                    }
                    alert('Ошибка при передаче данных!');
                    updatePage();
                }
            });
        }, timer);

    }


    // Обработка нажатия кнопок
    // Увеличить/уменьшить количество товаров, отправка формы
    $('.btn').click(function(){
        // Отправка формы
        if ($(this).attr('name') == 'send') {
            if ($('#total_sum').html() != 0) {
                var change = 'send';
                change_and_send(change, [], 0);
            }
            return
        }

        // Уменьшить количество товаров
        var var_value = "#var-value_" + $(this).attr('id');
        var value = $(var_value).html();
        if ($(this).attr('name') == 'btn-minus') {
            value = (value=='1')?value:value-1;
        }
        // Увеличить количество товаров
        if ($(this).attr('name') == 'btn-plus') {
            value++;
        }
        $(var_value).html(value);
        var change = 'change';
        var product = [$(this).attr('id')];
        var timer = 500;
        change_and_send(change, product, timer);
    });


    // Удаление товара из корзины
    $('.manag').on('click', function(e){
        e.preventDefault(); // Отмена стандартного поведения перехода по ссылке
        var change = 'delete';
        var product = [$(this).attr('id')];
        var timer = 0;
        change_and_send(change, product, timer);
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
        var all = $(".form-check-input"); // Находим все товары по чекбоксам
        var product = [];
        $.each(all,function(id, obj) {
            if (obj.checked) {
                product.push(obj.name)
            }
        });
        var change = 'delete';
        var timer = 0;
        change_and_send(change, product, timer);

    });


    // Пересчет сумм при выборе или снятии выбора товаров
    $(".form-check-input").on('change', function(){
        updatePage()
    });


    // Подготовка содержимого корзины для отправки на сервер и отправка
    // Функция готовит будущее корзины, запоминает ключевые показатели
    // Применяет изменения после удачного согласования с сервером или отменяет их
    // Аргумент change может быть: 'change' - изменение одного товара, 'delete' - удаление товаров
    // 'send' - подготовка списка для отправки
    // Аргумент product содержит список изменяемых товаров или ничего: 'change'
    function change_and_send(change, product, timer){
        var all = $(".form-check-input") // Находим все товары по чекбоксам
        // console.log(change, product);
        const data = {}; // Данные для отправки
        $.each(all,function(id, obj) {
            var sel_quanity = '#var-value_' + obj.name // id количества товара
            if (!(product.includes(obj.name) && change == 'delete')) {
                // Товар не отправляется если он кандидат на удаление
                if (change != 'send' || (change == 'send' && obj.checked)) {
                    // Товар отправляется всегда при обновлении
                    // И только при установленном checked если это заказ (send)
                    data[obj.name] = $(sel_quanity).html() // Создаем массив id: количество
                }
            }
        });
        sendCanges(data, change, product, timer);
    };

});