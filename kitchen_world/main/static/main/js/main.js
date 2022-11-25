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
