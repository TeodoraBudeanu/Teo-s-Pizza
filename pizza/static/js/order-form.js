$(document).ready(function(){
  var order_id = document.getElementById("order").innerHTML;



  $.when(
    $.get("get_order", {id : order_id }),
    $.get("get_pizzas")
  ).then(
    function(order, pizzas){
      var pizza_types = [];
      pizzas[0].forEach(myFunction);
      function myFunction(item){
        pizza_types.push(item.name);
      }

      $('form').jsonForm({
        schema: {
          type: "object",
          required: ["address", "order_items"],
          properties: {
            address: {type: 'string'},
            comment: {type: 'string'},
            order_items: {
              type: 'array',
              items: {
                type: "object",
                required: ["pizza_type", "quantity"],
                properties: {
                  pizza_type:{type: "string" , enum: "P" },
                  quantity: {type: "integer", default: 1},
                },
              },
            },
          },
        },
        uiSchema: {
          type: "VerticalLayout",
          elements:[
            {
              type: "Control",
              label: "Address",
              scope: {"$ref": "#/properties/address"}
            },
            {
              type: "Control",
              label: "Comment",
              scope: "#/properties/comment"
            },
           ],
        },
        form: [
          "*",
          {
            type: "submit",
            title: "Save Order",
          }
        ],
        value: order[0],
        onSubmit: function (errors, values) {
           if (errors) {
             alert(errors);
           }
           else {
             alert("OK");
           }
         }
      });
            $("select[id*='pizza_type']").change(function(){
              console.log($(this).find(".select :selected").text());
              $.get("get_stock", {name: $(this).innerHTML}).done(
                function(stock){
                  console.log($(this).innerHTML);
                  console.log(stock);
                }
              )
            });
          }
        ).fail(function(err) {
          console.error('Oops', err);
        });
      });
/*  $.ajax({
    type:"GET",
    url: "place_order",
    data: { name: pizza },
    async: true,
    datatype: "text",
    success: function(data){
      total = total + data * quantity;
      $("#output1").val(total);
      if ($("#output1").val()>0) {
        $('.submit-button').prop('disabled', false);
      }
    }});

  calculate_total();

  if ($("#output1").val()>0) {
      $('.submit-button').prop('disabled', false);
  }

  $(".form-row").change(function(){
    calculate_total();
  });

  function calculate_total(){
    var total = 0;
    $(".form-row").each(function(){
      var price = 0;
      var pizza = $(this).find(".select :selected").text();
      var quantity = $(this).find("input").val();

      if (!quantity>0){
        $("#output1").val(total);
        if ($("#output1").val()==0){
          $('.submit-button').prop('disabled', true);
        };
      }
      else if (pizza!="---------" && quantity>0){
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
    deleteForm('form', $(this));
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

  function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 1){
        btn.closest('.form-row').remove();
        var forms = $('.form-row');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
            $(forms.get(i)).find(':input').each(function() {
                updateElementIndex(this, prefix, i);
            });
        }
    }
    return false;
}
});*/
