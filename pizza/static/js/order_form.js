$(document).ready(function(){

  var order_id = $("#order_id").text();
  $('.submit-button').prop('disabled', true);
  check_total();

  function check_total(){
    $.ajax({
      type: "GET",
      url: 'check_total',
      data: {order_id: order_id},
      success: function(data){
        if (Number.isInteger(data)){
          if (data>0) {
            $('.submit-button').prop('disabled', false);
          }
          else {
            $('.submit-button').prop('disabled', true);
          }
        }
      }
    });
  }

  $(document).on('change', 'div[name=order_item]', function(){
    pizza_id = $(this).find(':selected').val();
    quantity = $(this).find('input[name=quantity]').val();
    console.log(quantity);
    elem = $(this);
    if (quantity == ''){
      elem.find('.response').html("<span class='not-exists'>Please select the desired quantity.</span>");
      $('.submit-button').prop('disabled', true);
    }
    else {
      $.ajax({
        type: "GET",
        url: 'check_stock',
        data: {pizza_id: pizza_id, quantity: quantity},
        success: function(data){
          if (data == 'ok'){
              save_order();
              elem.find('.response').html("");
            }
            else {
              elem.find('.response').html("<span class='not-exists'>"+ data +"</span>");
            }
          }
        });
    }

  });

  function save_order(){
    var order_data = $("#orderForm").serialize();
    var order_item_data = $("#orderItemsForm").serialize();

    $.ajax({
      type: "GET",
      url: 'save_order',
      data: {order_data: order_data, order_item_data: order_item_data, order_id: order_id},
      success: function(data){
        if (Number.isInteger(data)){
          $("#output1").val(data);
          if (data>0) {
            $('.submit-button').prop('disabled', false);
          }
          else {
            $('.submit-button').prop('disabled', true);
            };
          }
        }
    });
  };

  $(document).on('click', '.add-form-row', function(e){
    e.preventDefault();
    cloneMore('div[name=order_item]:last');
    return false;
  });

  function cloneMore(selector) {
    var newElement = $(selector).clone();
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
        var name = $(this).attr('name')
        if(name) {
            $(this).attr({'name': name}).val('').removeAttr('selected');
        }
    });
    newElement.find('label').each(function() {
        var forValue = $(this).attr('for');
        if (forValue) {
          $(this).attr({'for': forValue});
        }
    });

    $(selector).after(newElement);
    var conditionRow = $('.form-row:not(:last)');
    conditionRow.find('.btn.add-form-row')
    .removeClass('btn-success').addClass('btn-danger').addClass('btn-block')
    .removeClass('add-form-row').addClass('delete-form-row')
    .html('Delete this item');
    return false;
  }

  $(document).on('click', '.delete-form-row', function(e){
    e.preventDefault();
    deleteForm($(this));
    return false;
});

  function deleteForm(btn) {
    var oi = 0
    $(".pizza").each(function(){
      oi++;
    });
    if (oi > 1){
      btn.attr({'id': 'item'})
      elem = document.getElementById("item");
      elem.parentNode.parentNode.parentNode.parentNode.removeChild(elem.parentNode.parentNode.parentNode);
      save_order();
    }
    return false;
}

$("#confbtn").click(function(e){
  e.preventDefault();
  window.location.href = "confirm_order";
});

});
