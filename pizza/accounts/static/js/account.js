$(document).ready(function(){

  $(".fa-edit").click(function(){
    $(".alignright").show();
    $(".collapse").collapse('hide');
    $(this).parent().hide();
  });

  $(".cancel").click(function(){
    $(".collapse").collapse('hide');
    $(".alignright").show();
  });

  $(".confirm").click(function(){
    $(".collapse").collapse('hide');
    $(".alignright").show();
  });

  $("#delete-account").click(function(){
    $.ajax({
      type: "get",
      url: "account_delete"
    }).done(window.location.replace("http://127.0.0.1:8000"));
  });

});
