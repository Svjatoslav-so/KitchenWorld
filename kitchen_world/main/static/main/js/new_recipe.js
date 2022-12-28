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
const previewBlock = document.getElementById('recipe-images-small-wrapper')
let swiper1;

function loadMainPhoto(event){
    //delete old version of preview

    if(swiper1) swiper1.destroy(true,false);

    let oldSlides = slides.querySelectorAll(".swiper-slide");
    for(let i = 0; i < oldSlides.length ; i++){
        if(oldSlides[i].className.indexOf("new-swiper-slide") == -1){
            slides.removeChild(oldSlides[i]);
        }
    }
    previewBlock.replaceChildren();

    const imageFiles = event.target.files;
    const imageFilesLength = imageFiles.length;

    console.log("FOTO ADDED");
    console.log(src.value);
    console.log(event.target.files);
    console.log("___________");

    for(let i = 0; i < imageFilesLength; i++){
        if(imageFiles[i].type.startsWith("image")){
            const imageSrc = URL.createObjectURL(imageFiles[i]);
            slides.innerHTML += '<div class="swiper-slide"><img src="' + imageSrc + '" alt="photo-of-recipe"></div>';
            // add preview image
            let newpreviewImg = document.createElement("div");
            newpreviewImg.className = "image-preview";
            newpreviewImg.innerHTML = `<img src="${imageSrc}" alt="photo-of-recipe"></img>`;
            previewBlock.appendChild(newpreviewImg)
            console.log("sucses");
        }
        else{
            // delete imageFiles[i];
            src.value = "";
            console.log("delete");
        }
    }

    swiper1 = new Swiper('.recipe-images__swiper', {
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
}


let stepsBlock = document.getElementById("steps-block");
let addStepBtn = document.getElementById("add-step");

/* ------------ Добавление нового шага рецепта --------------- */
addStepBtn.onclick = function(){
    let id = stepsBlock.children.length + 1;
    newStep = document.createElement("div");
    newStep.className = "new-step";
    newStep.id = id;
    newStep.innerHTML =`<div class="new-step__desc">
             <div class="step-wrapper">
                 <input class="section-title section-title_left" name="step-title" value="Шаг ${id}" required>
                 <button type="button" class="btn-delete" onclick="deleteStep(this)"></button>
             </div>
             <textarea class="input auto" rows="10" name="step-description"></textarea>
         </div>
         <div class="new-step-img">
             <label><input name="step_photo" type="file" accept="image/png, image/jpeg" required onchange="loadStepPhoto(this, event)"></label>
         </div>`
    stepsBlock.appendChild(newStep);
}

/* ------------ Удаление шага рецепта --------------- */
function deleteStep(elem){
    let parent = elem.closest(".new-step");
    stepsBlock.removeChild(parent);
}

/* ------------ Загрузка картинки к шагу рецепта --------------- */
function loadStepPhoto(elem, event){
    console.log(elem);
    console.log(event);
    let file = event.target.files[0];
    console.log(file);
    if (file.type.startsWith("image")){
        let imageSrc = URL.createObjectURL(file);
        console.log(imageSrc);
        elem.closest(".new-step-img").style.background = `url(${imageSrc}) no-repeat center center/cover`
    }
    else{
        console.log("MakeEmpty")
        event.target.value = "";
    }
}


/* -------- Установка статуса рецепта перед отправкой в зависимомти от нажаной кнопки ------ */
function toDraftsRecipe(elem){
    elem.parentElement.firstElementChild.value = "to_drafts";
    
}
function publishRecipe(elem){
    elem.parentElement.firstElementChild.value = "publish";

}

/* -------- Добавление новой категории ---------- */
let categoryMakerInput = document.getElementById("category_maker");
let categoryAutocompleteList = document.getElementById("category-autocomplete-list");
let addCategoryBtn = document.getElementById("add-category-btn");
let categoriesTags = document.getElementById("categories-tags");

categoryMakerInput.oninput = categoryAutocomplete;
// categoryMakerInput.onmouseover = categoryAutocomplete;
categoryAutocompleteList.onmouseleave = hideCategoryAutocompleteList;
function hideCategoryAutocompleteList(){
    deleteAllAutocompleteLi(categoryAutocompleteList);
}

function deleteAllAutocompleteLi(elem){
    elem.replaceChildren();
}

function setCategory(){
    categoryMakerInput.value = this.innerHTML;
    deleteAllAutocompleteLi(categoryAutocompleteList);    
}

function categoryAutocomplete(){
    let val = this.value ? this.value.toLowerCase() : this.value;
    deleteAllAutocompleteLi(categoryAutocompleteList);
    if (val){
        for(let i = 0; i < categoriesList.length; i++){
            if(categoriesList[i].toLowerCase().indexOf(val) != -1){
                let newLi = document.createElement('li');
                newLi.innerHTML = categoriesList[i];
                newLi.onclick = setCategory;
                categoryAutocompleteList.appendChild(newLi);
            }
        }
    }
}

addCategoryBtn.onclick = function(){
    if(categoriesList.includes(categoryMakerInput.value)){
        let newCatTag = document.createElement("div");
        newCatTag.className = "category-wrapper";
        newCatTag.innerHTML = `<button type="button" class="btn-delete" onclick="deteteCategory(this)"></button>
        <p class="category category_light">#${categoryMakerInput.value.toLowerCase()}</p>
        <input type="hidden" name="category" value="${categoryMakerInput.value}">`;
        categoriesTags.insertBefore(newCatTag, categoryMakerInput.closest(".new-category-wpapper"));
    }
    categoryMakerInput.value = "";
}

function deteteCategory(elem){
    categoriesTags.removeChild(elem.closest(".category-wrapper"));
}



/*-------------------------------------------------------------------
      БЛОК КОДА ПОСВЯЩЕННЫЙ ВЗАИМОДЕЙСТВИЮ С ИНГРЕДИЕНТАМИ
 --------------------------------------------------------------------*/

        /* ----------- Редактирование ингредиента ------------ */
        function editIngredient(elem){
            /* Отменяем предыдушее редактирование если такое было */
            cancelEditIngredient();
            /* Удаляем блок добавления аналога если такой есть */
            let oldanalogBlock = document.getElementById("new_analog_block");
            if(oldanalogBlock) ingredientList.removeChild(oldanalogBlock);

            let newIngredientBlock = document.getElementById("new_ingredient_block");
            newIngredientBlock.style.display = "none";
            let ingredietnBlock = elem.closest(".ingredient");
            ingredietnBlock.id = "is_edited";
            let editBlock = document.createElement("div");
            editBlock.className = "add-new-ingredient";
            editBlock.id = "edit-block";
            editBlock.innerHTML = `<div class="add-new-ingredient">
                <div class="add-new-ingredient__inner">
                    <div class="product-autocomplete">
                        <input class="input input-420 prod-auto-input" type="text"
                            placeholder="Название ингредиента" value="${ingredietnBlock.querySelector('input[data-content="product_name"]').value}" id="ingredient_maker">
                        <ul class="autocomplete-items" id="product-autocomplete-list">
                        </ul>
                    </div>
                    <div class="ingredient-params__param">
                        <input type="text" value="${ingredietnBlock.querySelector('input[data-content="quantity"]').value}" oninput="numberOnly(this)" class="input small-input" id="ingredient-weight">
                        <input type="text" value="${ingredietnBlock.querySelector('input[data-content="quantity"]+p').innerHTML}" class="input small-input"
                            id="ingredient-units" readonly>
                    </div>
                </div>
                <textarea class="input auto" cols="30" rows="4" id="ingredient-comment"
                    placeholder="Комментарий к ингредиенту">${ingredietnBlock.querySelector('input[data-content="product_comment"]').value}</textarea>
                <div class="ingredient-params__param ingredient-params__param-right">
                    <button type="button" class="btn-green btn-green-ghost"
                        onclick="cancelEditIngredient()">Отменить</button>
                    <button type="button" class="btn-green" onclick="applyEditIngredient()">Изменить</button>
                </div>
            </div>`;
            ingredientList.insertBefore(editBlock, ingredietnBlock);
            /* переопределяем переменные необходимые для автозаполнения и добавления нового шага */
            ingredientMakerInput = document.getElementById("ingredient_maker");
            ingredientMakerInput.oninput = productAutocomplete;
            productAutocompleteList = document.getElementById("product-autocomplete-list");
            ingredientWeight = document.getElementById("ingredient-weight");
            ingredientDimension = document.getElementById("ingredient-units");
            ingredientComment = document.getElementById("ingredient-comment");

            ingredietnBlock.style.display = "none"; 
        }

        /* ----------- Отмена редактирования ингредиента ------------ */
        function cancelEditIngredient(){
            let ingredietnBlock = document.getElementById("is_edited");
            let editBlock = document.getElementById("edit-block");
            if(ingredietnBlock && editBlock){
                let newIngredientBlock = document.getElementById("new_ingredient_block");
                newIngredientBlock.style.display = "block";
                ingredientList.removeChild(editBlock);
                ingredietnBlock.style.display = "flex";
                ingredietnBlock.id = "";
                /* переопределяем переменные необходимые для автозаполнения и добавления нового шага */
                ingredientMakerInput = document.getElementById("ingredient_maker");
                ingredientMakerInput.oninput = productAutocomplete;
                productAutocompleteList = document.getElementById("product-autocomplete-list");
                ingredientWeight = document.getElementById("ingredient-weight");
                ingredientDimension = document.getElementById("ingredient-units");
                ingredientComment = document.getElementById("ingredient-comment");
            }
        }
        /* ----------- Применить редактирование ингредиента ------------ */
        function applyEditIngredient(){
            let ingredietnBlock = document.getElementById("is_edited");
            let editBlock = document.getElementById("edit-block");
            if(ingredietnBlock && editBlock){
                let newIngredientBlock = document.getElementById("new_ingredient_block");
                newIngredientBlock.style.display = "block";
                ingredietnBlock.style.display = "flex";
                ingredietnBlock.id = "";
                console.log(ingredientMakerInput.value);
                if(ingredientDimension.value != "" && ingredientMakerInput.value != ""){
                    console.log("Ingr ",ingredientMakerInput.value);
                    ingredietnBlock.querySelector('input[data-content="product_name"]').value = ingredientMakerInput.value;
                    ingredietnBlock.querySelector('input[data-content="product_name"]+h3').innerHTML = ingredientMakerInput.value;
                    ingredietnBlock.querySelector('input[data-content="quantity"]+p').innerHTML = ingredientDimension.value;
                }
                if(ingredientWeight.value != ""){
                    console.log("Wei ",ingredientWeight.value);
                    ingredietnBlock.querySelector('input[data-content="quantity"]').value = ingredientWeight.value;
                }
                console.log("Com ",ingredientComment.value);
                if(ingredientComment.value != ""){
                    console.log("Comm ",ingredientComment.value);
                    ingredietnBlock.querySelector('input[data-content="product_comment"]').value = ingredientComment.value;
                    ingredietnBlock.querySelector('input[data-content="product_comment"]+p').innerHTML = ingredientComment.value;
                }
                ingredientList.removeChild(editBlock);
                /* переопределяем переменные необходимые для автозаполнения и добавления нового шага */
                ingredientMakerInput = document.getElementById("ingredient_maker");
                ingredientMakerInput.oninput = productAutocomplete;
                productAutocompleteList = document.getElementById("product-autocomplete-list");
                ingredientWeight = document.getElementById("ingredient-weight");
                ingredientDimension = document.getElementById("ingredient-units");
                ingredientComment = document.getElementById("ingredient-comment");
            }
        }

        /* ------ Удаление нового ингредиента ------ */
        function deleteIngredient(elem){
            let ingredient = elem.closest(".ingredient");
            if(ingredient.querySelector(".ingredient-number")){
                let num = ingredient.querySelector(".ingredient-number").innerHTML;
                console.log("num ", num);
                let ingredients = document.querySelectorAll(".ingredient")
                for(let i = 0; i < ingredients.length; i++){
                    console.log("ch ", ingredients[i]);
                    if(ingredients[i].dataset.parent_ingredient_id == num){
                        console.log("ch-d ", ingredients[i]);
                        ingredientList.removeChild(ingredients[i]);
                    }
                }
            }
            //если удаляенный ингредиент не аналог то правим индексы
            if(!ingredient.dataset.parent_ingredient_id && ingredient.nextElementSibling){
                updateIndex(ingredient.nextElementSibling);
            }
            ingredientList.removeChild(ingredient);
            // updateIndex(ingredient.nextElementSibling);
        }

        /* ---- После удаления ингредиента правит индексы в ниже идуших ингредиентах и их аналогах------ */
        function updateIndex(elem){
            console.log(elem);
            let ingredientNumber =  elem.querySelector(".ingredient-number");
            if(ingredientNumber){
                ingredientNumber.innerHTML = +ingredientNumber.innerHTML - 1
            }
            let allInputs = elem.querySelectorAll("input");
            for(let i=0; i<allInputs.length; i++){
                if(allInputs[i].name.indexOf("analog") != -1){
                    old_index = allInputs[i].name.split('-')[1];
                    console.log("old_index ", old_index, " old_index-1",  old_index - 1);
                    allInputs[i].name = allInputs[i].name.replace(old_index, old_index - 1);
                }
            }
            if(elem.dataset.parent_ingredient_id){
                elem.dataset.parent_ingredient_id = elem.dataset.parent_ingredient_id - 1;
            }

            if(elem.nextElementSibling){
                updateIndex(elem.nextElementSibling);
            }
        }

        function addAnalog(elem){
            /* Отменяем предыдушее редактирование если такое было */
            cancelEditIngredient();
            /* Удаляем предыдуший блок добавления аналога если такой есть */
            let oldanalogBlock = document.getElementById("new_analog_block");
            if(oldanalogBlock) ingredientList.removeChild(oldanalogBlock);

            let analogBlock = document.createElement("div");
            analogBlock.className = "add-new-ingredient";
            analogBlock.id = "new_analog_block";
            analogBlock.innerHTML = `<div class="add-new-ingredient__inner">
                <div class="product-autocomplete">
                    <input class="input input-420 prod-auto-input" type="text"
                        placeholder="Название ингредиента" value="" id="ingredient_maker">
                    <ul class="autocomplete-items" id="product-autocomplete-list">
                    </ul>
                </div>
                <div class="ingredient-params__param">
                    <input type="text" value="" oninput="numberOnly(this)" class="input small-input" id="ingredient-weight">
                    <input type="text" value="" class="input small-input"
                        id="ingredient-units" readonly>
                </div>
            </div>
            <textarea class="input auto" cols="30" rows="4"
                placeholder="Комментарий к ингредиенту" id="ingredient-comment"></textarea>
            <div class="ingredient-params__param ingredient-params__param-right">
                <button type="button" class="btn-green btn-green-ghost"
                            onclick="canceladdAnalog()">Отменить</button>
                <button type="button" class="btn-green" onclick="addNewIngredient(${elem.closest(".ingredient").querySelector(".ingredient-number").innerHTML})">Добавить аналог</button>
            </div>`;
            if(elem.closest(".ingredient").nextElementSibling){
                ingredientList.insertBefore(analogBlock, elem.closest(".ingredient").nextElementSibling);
            }
            else{
                ingredientList.appendChild(analogBlock);
            }
            let newIngredientBlock = document.getElementById("new_ingredient_block");
            newIngredientBlock.style.display = "none";
            /* переопределяем переменные необходимые для автозаполнения и добавления нового шага */
            ingredientMakerInput = document.getElementById("ingredient_maker");
            ingredientMakerInput.oninput = productAutocomplete;
            productAutocompleteList = document.getElementById("product-autocomplete-list");
            ingredientWeight = document.getElementById("ingredient-weight");
            ingredientDimension = document.getElementById("ingredient-units");
            ingredientComment = document.getElementById("ingredient-comment");
        }

        function canceladdAnalog(){
            analogBlock = document.getElementById("new_analog_block");
            ingredientList.removeChild(analogBlock);
            let newIngredientBlock = document.getElementById("new_ingredient_block");
            newIngredientBlock.style.display = "block";
            /* переопределяем переменные необходимые для автозаполнения и добавления нового шага */
            ingredientMakerInput = document.getElementById("ingredient_maker");
            ingredientMakerInput.oninput = productAutocomplete;
            productAutocompleteList = document.getElementById("product-autocomplete-list");
            ingredientWeight = document.getElementById("ingredient-weight");
            ingredientDimension = document.getElementById("ingredient-units");
            ingredientComment = document.getElementById("ingredient-comment");
        }

        /* -------- Добавление нового ингредиента ---------- */
            let ingredientList = document.getElementById("ingredient-list");
            let ingredientWeight = document.getElementById("ingredient-weight");
            let ingredientDimension = document.getElementById("ingredient-units");
            let ingredientMakerInput = document.getElementById("ingredient_maker");
            let ingredientComment = document.getElementById("ingredient-comment");
            let productAutocompleteList = document.getElementById("product-autocomplete-list");
            let addNewIngredientBtn = document.getElementById("add-new-ingredient");

            /* -------- Добавление продукта в новый ингредиент ---------- */
            ingredientMakerInput.oninput = productAutocomplete;

            function productAutocomplete(){
                let val = this.value.toLowerCase();
                deleteAllProductAutocompleteLi(productAutocompleteList);
                if (val){
                    for(let i = 0; i < productsList.length; i++){
                        if(productsList[i][0].toLowerCase().indexOf(val) != -1){
                            let newLi = document.createElement('li');
                            newLi.innerHTML = productsList[i][0];
                            newLi.dataset.prod_id = i;
                            newLi.onclick = setProduct;
                            productAutocompleteList.appendChild(newLi);
                        }
                    }
                }
            }

            function deleteAllProductAutocompleteLi(elem){
                deleteAllAutocompleteLi(elem);
                ingredientDimension.value = "";
            }

            function setProduct(){
                ingredientMakerInput.value = this.innerHTML;
                deleteAllProductAutocompleteLi(productAutocompleteList);
                let num = this.dataset.prod_id;
                ingredientDimension.value = productsList[num][1];
                
            }

            /* ------ Добавляет новый ингредиент в список ингредиентов ------ */
            addNewIngredientBtn.onclick = addNewIngredient;
            function addNewIngredient(parentIngredientId=""){
                parentIngredientId = parseInt(parentIngredientId) != parseInt(parentIngredientId) ? "" : parseInt(parentIngredientId);
                ingredientDimension.style.borderColor = "#48B705";
                ingredientWeight.style.borderColor = "#48B705";
                ingredientMakerInput.style.borderColor = "#48B705";

                if(ingredientDimension.value && ingredientWeight.value){
                    let num = ingredientList.querySelector("[data-parent_ingredient_id]") ? ingredientList.children.length + 1 - ingredientList.querySelectorAll("[data-parent_ingredient_id]").length : ingredientList.children.length + 1;
                    let newIngredient = document.createElement("div");
                    newIngredient.className = "ingredient";
                    id = "";
                    if(parentIngredientId){
                        id = parentIngredientId;
                        newIngredient.dataset.parent_ingredient_id = id;
                        num = "";
                    }
                    newIngredient.innerHTML = `<div class="ingredient-info">
                    ${ parentIngredientId == "" ? `<div class="ingredient-number">${num}</div>` : ""}
                        <div class="ingredient-inner">
                            <input type="hidden" name="${parentIngredientId ? "analog-"+id+"-" : ""}product_name" value="${ingredientMakerInput.value}" required data-content="product_name">
                            <h3 class="ingredient-title">${ingredientMakerInput.value}</h3>
                            <input type="hidden" name="${parentIngredientId ? "analog-"+id+"-" : ""}product_comment" value="${ingredientComment.value}" required data-content="product_comment">
                            <p class="ingredient-desc">${ingredientComment.value}</p>
                        </div>
                    </div>

                    <div class="ingredient-params">
                        ${ parentIngredientId == "" ?
                        `<div class="ingredient-params__param">
                            <p class="info-paragraph required-ing">Обязательный</p>
                            <label class="switch">
                                <input type="text" name="is_essential" value="True">
                                <span class="switch__slider round on" onclick="isEssentialChecker(this)"></span>
                            </label>
                        </div>` : `<div class="ingredient-params__param"><p class="info-paragraph required-ing">Аналог</p></div>`}
                        <div class="ingredient-params__param">
                            <input type="text" value="${ingredientWeight.value}" name="${parentIngredientId ? "analog-"+id+"-" : ""}quantity" oninput="numberOnly(this)" class="input small-input" required data-content="quantity">
                            <p class="input small-input">${ingredientDimension.value}</p>
                        </div>
                        ${ parentIngredientId == "" ?
                        `<div class="ingredient-params__param">
                            <button type="button" class="btn-green" onclick="addAnalog(this)">Добавить
                                аналог</button>
                        </div>` : ""}
                        <div class="ingredient-params__param">
                            <button type="button" class="btn-delete" onclick="deleteIngredient(this)"></button>
                            <button type="button" class="btn-edit" onclick="editIngredient(this)"></button>
                        </div>
                    </div>`; 
                    if(parentIngredientId){
                        let analogBlock = document.getElementById("new_analog_block");
                        ingredientList.insertBefore(newIngredient, analogBlock);
                        ingredientList.removeChild(analogBlock);
                        let newIngredientBlock = document.getElementById("new_ingredient_block");
                        newIngredientBlock.style.display = "block";
                        /* переопределяем переменные необходимые для автозаполнения и добавления нового шага */
                        ingredientMakerInput = document.getElementById("ingredient_maker");
                        ingredientMakerInput.oninput = productAutocomplete;
                        productAutocompleteList = document.getElementById("product-autocomplete-list");
                        ingredientWeight = document.getElementById("ingredient-weight");
                        ingredientDimension = document.getElementById("ingredient-units");
                        ingredientComment = document.getElementById("ingredient-comment");
                    }
                    else{
                        ingredientList.appendChild(newIngredient);
                    }

                    ingredientMakerInput.value = "";
                    ingredientDimension.value = "";
                    ingredientWeight.value = "";
                    ingredientComment.value = "";
                }
                else{
                    if(ingredientDimension.value){
                        ingredientWeight.style.borderColor = "red";
                    }else if(ingredientWeight.value){
                        ingredientDimension.style.borderColor = "red";
                        ingredientMakerInput.style.borderColor = "red";
                    }
                    else{
                        ingredientDimension.style.borderColor = "red";
                        ingredientWeight.style.borderColor = "red";
                        ingredientMakerInput.style.borderColor = "red";
                    }
                }
            }

            /*------------------- Управляет инпутом основного ингредиента --------------------- */
            function isEssentialChecker(elem){
                let isEssential = elem.previousElementSibling;
                if (isEssential.value == "True"){
                    isEssential.value = "False";
                    elem.className = elem.className.replace(" on","");
                }
                else{
                    isEssential.value = "True";
                    elem.className += " on";
                }
            }


/* -------- Контролирует чтобы вводились только числа  ---------- */
function numberOnly(elem){
    elem.value = elem.value.replace(/[^\d]/g, '');
}


/*------------------- Получение списка продуктов и списка категорий-------------------*/
var productsList;
var categoriesList;

//Создаем функцию обработчик для загрузки списка продуктов
var loadProducts = function(Request)
{
    productsList = JSON.parse(Request.response);
}

//Создаем функцию обработчик для загрузки списка категорий
var loadCategories = function(Request)
{
    categoriesList = JSON.parse(Request.response);
    console.log(categoriesList);
}

SendRequest("GET","/get_products_with_dimension/", "", loadProducts);
SendRequest("GET","/get_all_categories/", "", loadCategories);

function CreateRequest()
{
    var Request = false;

    if (window.XMLHttpRequest)
    {
        //Gecko-совместимые браузеры, Safari, Konqueror
        Request = new XMLHttpRequest();
    }
    else if (window.ActiveXObject)
    {
        //Internet explorer
        try
        {
             Request = new ActiveXObject("Microsoft.XMLHTTP");
        }    
        catch (CatchException)
        {
             Request = new ActiveXObject("Msxml2.XMLHTTP");
        }
    }
 
    if (!Request)
    {
        alert("Невозможно создать XMLHttpRequest");
    }
    
    return Request;
} 

/*
Функция посылки запроса к файлу на сервере
r_method  - тип запроса: GET или POST
r_path    - путь к файлу
r_args    - аргументы вида a=1&b=2&c=3...
r_handler - функция-обработчик ответа от сервера
*/
function SendRequest(r_method, r_path, r_args, r_handler)
{
    //Создаём запрос
    var Request = CreateRequest();
    
    //Проверяем существование запроса еще раз
    if (!Request)
    {
        return;
    }
    
    //Назначаем пользовательский обработчик
    Request.onreadystatechange = function()
    {
        //Если обмен данными завершен
    if (Request.readyState == 4)
    {
        if (Request.status == 200)
        {
            //Передаем управление обработчику пользователя
            // alert("Передаем управление обработчику пользователя")
            r_handler(Request);
        }
        else
        {
            //Оповещаем пользователя о произошедшей ошибке
            alert("Оповещаем пользователя о произошедшей ошибке")
        }
    }
    else
    {
        //Оповещаем пользователя о загрузке
        // alert("Оповещаем пользователя о загрузкее")
    }
    }
    
    //Проверяем, если требуется сделать GET-запрос
    if (r_method.toLowerCase() == "get" && r_args.length > 0)
    r_path += "?" + r_args;
    
    //Инициализируем соединение
    Request.open(r_method, r_path, true);
    
    if (r_method.toLowerCase() == "post")
    {
        //Если это POST-запрос
        
        //Устанавливаем заголовок
        Request.setRequestHeader("Content-Type","application/x-www-form-urlencoded; charset=utf-8");
        //Посылаем запрос
        Request.send(r_args);
    }
    else
    {
        //Если это GET-запрос
        Request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        //Посылаем нуль-запрос
        Request.send(null);
    }
} 



