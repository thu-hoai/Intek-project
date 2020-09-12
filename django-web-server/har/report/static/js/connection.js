
function toggleEyeShowPass() {
  let eyeShowPass = document.querySelector(".main_box_form_password_input");
  if (eyeShowPass.type === "password") {
    eyeShowPass.type = "text";
    document.getElementById("iconShowPass").className = "fa fa-eye"
  } else {
    eyeShowPass.type = "password";
    document.getElementById("iconShowPass").className = "fa fa-eye-slash"
  }
}

