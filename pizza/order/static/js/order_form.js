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
        if (data>0) {
          $("#output1").val(data);
          $('.submit-button').prop('disabled', false);
        }
        else {
          $('.submit-button').prop('disabled', true);
        }
      }
    });
  }

  $(document).on('change', '#orderForm', function(){
    var address = $(this).find('input[name=address]').val();
    var comment = $(this).find('textarea[name=comment]').val();
    var elem = $(this);
    if (address == ''){
      $('#address_response').html("<span class='not-exists'>Please type in your address.</span>");
      $('.submit-button').prop('disabled', true);
    }
    else {
      $.ajax({
        type: "get",
        url: 'save_order',
        data: {order_id: order_id, address: address, comment: comment}
      });
    }

  });

  $(document).on('change', 'div[name=order_item]', function(){
    var pizza_id = $(this).find(':selected').val();
    var quantity = $(this).find('input[name=quantity]').val();
    var elem = $(this);
    var item_id = elem.attr('value');
    if (quantity == '' || quantity <= 0){
      elem.find('.response').html("<span class='not-exists'>Please select the desired quantity.</span>");
      $("#output1").val(0);
      $('.submit-button').prop('disabled', true);
    }
    else {
      save_item(item_id, pizza_id, quantity);
    }

  });

  function save_item(item_id, pizza_id, quantity){
    $.ajax({
      type: "GET",
      url: 'save_item',
      data: {item_id: item_id, pizza_id: pizza_id, quantity: quantity},
      success: function(data){
        if (isNaN(data)){
          elem.find('.response').html("<span class='not-exists'>"+ data +"</span>");
          $('.submit-button').prop('disabled', true);
        }
        else {
          $("#output1").val(data);
          elem.find('.response').html("");
          $('.submit-button').prop('disabled', false);
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
    $.ajax({
      url: 'create_item',
      data: {old_item_id: newElement.attr('value')},
      type: 'GET',
      success: function(data){
        newElement.attr('value', data);
      }
    });

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
      btn.attr('id', 'item')
      var elem = document.getElementById("item");
      $.ajax({
        url: 'delete_item',
        data: {item_id: btn.parent().parent().parent().attr('value')},
        type: 'GET',
        success: function(data){
          elem.parentNode.parentNode.parentNode.parentNode.removeChild(elem.parentNode.parentNode.parentNode);
        }
      });
    }
    return false;
}

$("#confbtn").click(function(e){
  e.preventDefault();
  window.location.href = "confirm_order";
});

});
