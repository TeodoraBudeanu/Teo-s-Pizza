$(document).ready(function(){

    $("#username").keyup(function(){
      var username = $("#username").val();
      if (username != '') {
        $("#username_response").show();
        $.get('check_username', { username: username }, function(response){
            console.log(response);
            if(response > 0){
                $("#username_response").html("<span class='not-exists'>* Username already in use.</span>");
                username_is_valid = false;
            } else {
                $("#username_response").html("<span class='exists'>Available.</span>");

                username_is_valid = true;
            };
          });
      } else {
        $("#username_response").hide();
      }
    });

  $("#passwordtest").keyup(function(){
    password = $("#password").val();
    passwordtest = $("#passwordtest").val()
    if (passwordtest != '') {
      if (password == passwordtest) {
        $("#pass_response").html("<span class='equal'>* Passwords match.</span>");
        pass_match = true;
      } else {
        $("#pass_response").html("<span class='not-equal'>* Passwords do not match.</span>");
        pass_match = false;
      }
    } else {
      $("#pass_response").hide();
    }
  });
});
