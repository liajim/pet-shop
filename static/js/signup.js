$(document).ready(function() {
    $("form[name='registration']").submit(function(e) {
        e.preventDefault();
    }).validate({
        // Specify validation rules
        rules: {
          // The key name on the left side is the name attribute
          // of an input field. Validation rules are defined
          // on the right side
          first_name: "required",
          last_name: "required",
          username: {
            required: true,
            minlength: 5
          },
          email: {
            required: true,
            // Specify that email should be validated
            // by the built-in "email" rule
            email: true
          },
          address: "required",
          phone_number: "required",
          password: {
            required: true,
            minlength: 5
          },
          confirm_password: {
            equalTo: "#password"
          }
        },
        // Specify validation error messages
        messages: {
          first_name: "Please enter your firstname",
          last_name: "Please enter your lastname",
          username: {
            required: "Please provide a user name",
            minlength: "Your username must be at least 5 characters long"
          },
          address: "Please enter your address",
          phone_number: "Please enter your phone",
          password: {
            required: "Please provide a password",
            minlength: "Your password must be at least 5 characters long"
          },
          confirm_password: "Enter Confirm Password Same as Password",
          email: "Please enter a valid email address"
        },
        // Make sure the form is submitted to the destination defined
        // in the "action" attribute of the form when valid
        submitHandler: function(form) {
            var spinner = $('#spinner');
            spinner.modal('show');
            var data =  $(form).serializeArray();
            var data_to_send = {}
            for(var i =0; i<data.length;i++){
                data_to_send[data[i].name] = data[i].value
            }
            addCustomer(data_to_send,
                (data) => {
                    swal("Created!", "", "success");
                    spinner.modal('hide');
                    $('body').removeClass('modal-open');
                    $('.modal-backdrop').remove();
                    spinner.hide();
                    window.location = window.location.origin + '/login/'
                },
                (xhr, status, error) => {
                    swal("Error", xhr.responseText.substring(0, 400), "error");
                    console.log(xhr, error);
                    spinner.modal('hide');
                    $('body').removeClass('modal-open');
                    $('.modal-backdrop').remove();
                    spinner.hide();
                }
            );
        }
    });
})