$(document).ready(function() {
  $("body").toggleClass("sb-sidenav-toggled");
  $("#userDropdown").click((e) => {
    e.preventDefault();
    $("#menu-dropdown").toggle();
  })
});
