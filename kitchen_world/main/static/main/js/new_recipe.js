// ----------- Textarea -------------
document.querySelectorAll('textarea').forEach(el => {
    el.style.height = el.setAttribute('style', 'height: ' + el.scrollHeight + 'px');
    el.classList.add('auto');
    el.addEventListener('input', e => {
        el.style.height = 'auto';
        el.style.height = (el.scrollHeight) + 'px';
    });
});

// Preview images for slider
const src = document.getElementById('preview-images')
const slides = document.getElementById('swiper-wrapper')

src.addEventListener('change', (event) => {
    const imageFiles = event.target.files;
    const imageFilesLength = imageFiles.length;

    for(let i = 0; i < imageFilesLength; i++){
        const imageSrc = URL.createObjectURL(imageFiles[i]);
        slides.innerHTML += '<div class="swiper-slide"><img src="' + imageSrc + '" alt="photo-of-recipe"></div>';

    }

    let swiper1 = new Swiper('.recipe-images__swiper', {
        // Optional parameters
        direction: 'horizontal',
        loop: true,
        slidesPerView: 1,
        disableOnInteraction: false,
    
        autoplay: {
            delay: 3000,
            pauseOnMouseEnter: false,
        },
    
        });
})



