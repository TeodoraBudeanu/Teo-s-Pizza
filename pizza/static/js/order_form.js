$(document).ready(function(){

  $('.submit-button').prop('disabled', true);

  $(".form-row").change(function(){
    calculate_total();
  });

  $("#confbtn").click(function(e){
    e.preventDefault()
    var order_data = $("#orderForm").serialize();
    var order_item_data = $("#orderItemsForm").serialize();
    var order_id = $("#order_id").text();
    console.log(order_data);
    console.log(order_item_data);

    $.ajax({
      type: "GET",
      url: 'save_order',
      data: {order_data: order_data, order_item_data: order_item_data, order_id: order_id},
      success: function(data){
        console.log(data);
        window.location.href = data;
      },
    });
  });

  function calculate_total(){
    var total = 0;
    $(".form-row").each(function(){
      var price = 0;
      var pizza = $(this).find(".pizza :selected").text();
      var quantity = $(this).find("input").val();

      if (!quantity>0){
        $("#output1").val(total);
        if ($("#output1").val()==0){
          $('.submit-button').prop('disabled', true);
        };
      }
      else if (pizza!="--------" && quantity>0){
          $.ajax({
            type:"GET",
            url: "get_price",
            data: { name: pizza },
            async: true,
            datatype: "text",
            success: function(data){
              total = total + data * quantity;
              $("#output1").val(total);
              if ($("#output1").val()>0) {
                $('.submit-button').prop('disabled', false);
              }
            }})};
      });
  };

  $(document).on('click', '.add-form-row', function(e){
    e.preventDefault();
    cloneMore('.form-row:last', 'form');
    return false;
  });

  $(document).on('click', '.delete-form-row', function(e){
    e.preventDefault();
    deleteForm($(this));
    calculate_total();
    return false;
});

  function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
  }

  function cloneMore(selector, prefix) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
        var name = $(this).attr('name')
        if(name) {
            name = name.replace('-' + (total-1) + '-', '-' + total + '-');
            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        }
    });
    newElement.find('label').each(function() {
        var forValue = $(this).attr('for');
        if (forValue) {
          forValue = forValue.replace('-' + (total-1) + '-', '-' + total + '-');
          $(this).attr({'for': forValue});
        }
    });

    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
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
        // TODO: Find a way to delete parent
    }
    return false;
}
});
