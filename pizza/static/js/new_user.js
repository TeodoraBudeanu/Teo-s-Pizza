$(document).ready(function(){

  $('#signup').prop('disabled', true);
  username_is_valid = false;
  email_is_valid = false;
  pass_match = false;

  function check_form_validity(){
    if (email_is_valid && username_is_valid && pass_match) {
      $('#signup').prop('disabled', false);
    }
    else {
      $('#signup').prop('disabled', true);
    }
  }

  $("#username").keyup(function(){
    var username = $("#username").val();
    if (username != '') {
      $("#username_response").show();
      $.get('check_username', { username: username }, function(response){
          if(response > 0){
              $("#username_response").html("<span class='not-exists'>* Username already in use.</span>");
              username_is_valid = false;
          } else {
              $("#username_response").html("<span class='exists'>Available.</span>");
              username_is_valid = true;
          };
          check_form_validity();
        });
    } else {
      $("#username_response").hide();
    }
  });

  $("#email").change(function(){
    var email = $("#email").val();
    if (email != '') {
      $.get('check_email', { email: email }, function(response){
          if(response > 0){
            $("#email_response").show();
            $("#email_response").html("<span class='not-exists'>* Email already in use.</span>");
            email_is_valid = false;
          } else {
            $("#email_response").hide();
            email_is_valid = true;
          }
          check_form_validity();
        });
    } else {
      $("#email_response").hide();
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
    check_form_validity();
  });
});
