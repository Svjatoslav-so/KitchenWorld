$( document ).ready(function() {
  // ----------- Slider -------------
    const swiper = new Swiper('.new__swiper', {
        // Optional parameters
        direction: 'horizontal',
        loop: true,
        slidesPerView: 3,

        autoplay: {
            delay: 3000,
            pauseOnMouseEnter: false,
          },

      });

    const swiper1 = new Swiper('.recipe-images__swiper', {
    // Optional parameters
    direction: 'horizontal',
    loop: true,
    slidesPerView: 1,

    autoplay: {
        delay: 3000,
        pauseOnMouseEnter: false,
      },

    });

    //    Hide all analogs on start up
    $('.ingredient_analog').each(function(index){
        $(this).fadeOut(0);
    })

    $('.list-arrow').each(function(index){
    if($(this).parent().parent().children().length < 2)
        $(this).fadeOut()
    })


    $('.list-arrow').on('click', function(e){
        $(this).toggleClass('active')
        $(this).parent().parent().children('.ingredient_analog').each(function(index){
        $(this).fadeToggle();
        })
    })

});

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