function toggleModalOpen() {
  $("body").toggleClass("modal-open");
}

function loadRegisterForm() {
  $("#register-form").toggle();
  toggleModalOpen();
}

function closeRegisterForm() {
  $("#register-form").hide();
  toggleModalOpen();
}

function loadLoginForm() {
  $("#login-form").toggle();
  toggleModalOpen();
}

function closeLoginForm() {
  $("#login-form").hide();
  toggleModalOpen();
}

function loadAddGroupForm() {
  $("#addgroup-form").toggle();
  toggleModalOpen();
}

function closeAddGroupForm() {
  $("#addgroup-form").hide();
  toggleModalOpen();
}

function switchForm() {
  $("#login-form").toggle();
  $("#register-form").toggle();
}
