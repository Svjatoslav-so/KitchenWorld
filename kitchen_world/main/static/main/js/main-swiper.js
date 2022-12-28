$( document ).ready(function() {
  // ----------- Slider -------------
    const swiper = new Swiper('.new__swiper', {
      // Optional parameters
      direction: 'horizontal',
      loop: true,
      slidesPerView: 1,

      autoplay: {
          delay: 3000,
          pauseOnMouseEnter: false,
        },

      breakpoints: {
        // when window width is >= 675px
        675: {
          slidesPerView: 2
        },
        // when window width is >= 999px
        999: {
          slidesPerView: 3
        }
        // // when window width is >= 640px
        // 640: {
        //   slidesPerView: 4,
        //   spaceBetween: 40
        // }
      }

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
