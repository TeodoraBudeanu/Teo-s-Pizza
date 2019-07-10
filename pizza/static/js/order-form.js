$(document).ready(function(){

  $('button').prop('disabled', true);

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
          $('button').prop('disabled', true);
        };
      }
      else if (pizza!="---------" && quantity>0){
          $.ajax({
            type:"GET",
            url: "{% url 'get_price' %}",
            data: { name: pizza },
            async: true,
            datatype: "text",
            success: function(data){
              total = total + data * quantity;
              $("#output1").val(total);
              if ($("#output1").val()>0) {
                $('button').prop('disabled', false);
              }
            }})};
      });
  };
});
