
/* Открывашка закрывашка главного меню */
let navMenu = document.getElementById("nav-menu");

function showNavMenu(){
  navMenu.className += " active";
}
 
function closeNavMenu() {
  navMenu.className = navMenu.className.replace(" active", '');
}

navMenu.onmouseleave = closeNavMenu;
navMenu.ondblclick = closeNavMenu;
document.getElementById("close-nav-menu-btn").onclick = closeNavMenu;

/* Открывашка закрывашка меню на страницах профиля */
let profileMenu = document.getElementById("profile-menu");

if(profileMenu){
  function showProfileMenu(){
    profileMenu.className += " active";
  }
  
  function closeProfileMenu() {
    profileMenu.className = profileMenu.className.replace(" active", '');
  }

  profileMenu.onmouseleave = closeProfileMenu;
  profileMenu.ondblclick = closeProfileMenu;
  document.getElementById("close-profile-menu-btn").onclick = closeProfileMenu;
}