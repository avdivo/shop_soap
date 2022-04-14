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


    // Отправка формы
    form.on('submit', function(e){
        e.preventDefault(); // Отмена стандартного поведения Submit

        var quantity = $('#var-value').text();
        var product_id = $('#product_id').val();

        update_basket(product_id, quantity)

    });




});