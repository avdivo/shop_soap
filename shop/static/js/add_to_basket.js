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


    // Отправка формы для страницы shop по ссылке
    $('.btn').on('click', function(e){

        if ($(this).attr('name') == 'add'){
            e.preventDefault(); // Отмена стандартного поведения
            var product_id = $(this).attr('id');
            update_basket(product_id, 1)
        }

    });


    // Увеличить/уменьшить количество товаров
    $('#btn-minus').click(function(){
      var val = $("#var-value").html();
      val = (val=='1')?val:val-1;
      $("#var-value").html(val);
      $("#product-quanity").val(val);
      return false;
    });
    $('#btn-plus').click(function(){
      var val = $("#var-value").html();
      val++;
      $("#var-value").html(val);
      $("#product-quanity").val(val);
      return false;
    });

    // Accordion Меню выбора категорий
    var all_panels = $('.templatemo-accordion > li > ul').hide();

    $('.templatemo-accordion > li > a').click(function() {
        var target =  $(this).next();
        if(!target.hasClass('active')){
            all_panels.removeClass('active').slideUp();
            target.addClass('active').slideDown();
        }
      return false;
    });
    // End accordion

    $('.btn-size').click(function(){
      var this_val = $(this).html();
      $("#product-size").val(this_val);
      $(".btn-size").removeClass('btn-secondary');
      $(".btn-size").addClass('btn-success');
      $(this).removeClass('btn-success');
      $(this).addClass('btn-secondary');
      return false;
    });
});