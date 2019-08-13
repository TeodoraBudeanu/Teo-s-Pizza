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

      $("form").jsonForm({
        schema: {
          type: "object",
          properties: {
            id: {type: "integer"},
            address: {type: "string", minLength: 5, required: true},
            comment: {type: "string"},
            order_items: {
              type: "array",
              items: {
                type: "object",
                title: "Item",
                properties: {
                  pizza_type:{type: "string" , enum: pizza_types , minLength: 1, required: true},
                  quantity: {type: "integer", default: 1, minimum: 1,  maximum: 10, required: true},
                },
              },
            },
            user: {type: "integer"},
          },
        },
        form: [
          {
            key: "id",
            type: "hidden"
          },
          {
            key: "address",
            title: "Address"
          },
          {
            key: "comment",
            title: "Comment",
          },
          {
            type: "array",
            title: " ",
            items: [
              {
                type: "section",
                items: [{
                      key: "order_items[].pizza_type",
                      title: "Pizza",
                      htmlClass: "col-md-10 mb-0",
                    },
                    {
                      key: "order_items[].quantity",
                      title: "Quantity",
                      htmlClass: "col-md-2 mb-0"
                    },
              ]
            }
          ]
        },
        {
          key: "user",
          type: "hidden"
        },

        {
          type: "submit",
          title: "Confirm Order",
          htmlClass: "btn btn-success"
        }],
        value: order[0],
      });
    }
  ).fail(function(err) {
    console.error('Oops', err);
  });
});
