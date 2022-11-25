// ----------- Slider -------------
const swiper = new Swiper('.new__swiper', {
    // Optional parameters
    direction: 'horizontal',
    loop: true,
    slidesPerView: 3,
  
    autoplay: {
        delay: 3000,
        pauseOnMouseEnter: true,
      },

  });

const swiper1 = new Swiper('.recipe-images__swiper', {
// Optional parameters
direction: 'horizontal',
loop: true,
slidesPerView: 1,

autoplay: {
    delay: 3000,
    pauseOnMouseEnter: true,
  },

});