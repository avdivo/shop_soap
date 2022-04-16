// Добавление товара в корзину
$(document).ready(function(){
    var form = $('#form_work_basket');

// Ajax правление информации об обновлении корзины
function update_basket(product_id, quantity){
        var csrf_token = $('#form_work_basket [name="csrfmiddlewaretoken"]').val();
        var data = {
            'id': product_id,
            'quantity': quantity,
            'csrfmiddlewaretoken': csrf_token
        }

        var url = form.attr("action");

        console.log(data)
         $.ajax({
             url: url,
             type: 'POST',
             data: data,
             cache: true,
             success: function (data) {
                 console.log(data.products);
                 $('#quantity_in_basket').text(data.products);
                 console.log($('#quantity_in_basket').text());
             },
             error: function(){
                 console.log("error")
             }
         })

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


      // var val = $("#var-value").html();
      // val = (val=='1')?val:val-1;
      // $("#var-value").html(val);
      // $("#product-quanity").val(val);
      // return false;
    });
    // $('#btn-plus').click(function(){
    //   var val = $("#var-value").html();
    //   val++;
    //   $("#var-value").html(val);
    //   $("#product-quanity").val(val);
    //   return false;
    // });




    // Отправка формы для страницы shop по ссылке
    $('.btn').on('click', function(e){

        if ($(this).attr('name') == 'add'){
            e.preventDefault(); // Отмена стандартного поведения
            var product_id = $(this).attr('id');
            update_basket(product_id, 1)
        }

    });


});