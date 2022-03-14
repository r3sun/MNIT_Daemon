function show_user_menu(tag) {
  document.getElementById('user_menu').className = 'user_menu active';
  tag.setAttribute("onclick", "hide_user_menu(this)");
}

function hide_user_menu(tag) {
  document.getElementById('user_menu').className = 'user_menu';
  tag.setAttribute("onclick", "show_user_menu(this)");
}

function show_ntf() {
  document.getElementById('notification_container').classList.add("active");
}