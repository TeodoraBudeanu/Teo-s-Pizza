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
        console.log(data);
        if (Number.isInteger(data)){
          $("#output1").val(data);
          $('.submit-button').prop('disabled', false);
        }
      },
    });
  }

  $(document).on('change', '.form-row', function(){
    save_order();
  });

  function save_order(){
    var order_data = $("#orderForm").serialize();
    var order_item_data = $("#orderItemsForm").serialize();
    console.log($("#orderItemsForm").serialize());

    $.ajax({
      type: "GET",
      url: 'save_order',
      data: {order_data: order_data, order_item_data: order_item_data, order_id: order_id},
      success: function(data){
        console.log(data);
        if (Number.isInteger(data)){
          $("#output1").val(data);
          $('.submit-button').prop('disabled', false);

        }
      },
    });
  };

  $("#confbtn").click(function(e){
    e.preventDefault()
    window.location.href = "confirm_order";
  });

  $(document).on('click', '.add-form-row', function(e){
    e.preventDefault();
    console.log('div[name=order_item]:last');
    cloneMore('div[name=order_item]:last');
    return false;
  });

  $(document).on('click', '.delete-form-row', function(e){
    e.preventDefault();
    deleteForm($(this));
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
});
