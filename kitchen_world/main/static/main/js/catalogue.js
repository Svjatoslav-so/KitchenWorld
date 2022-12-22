/*----------------------- Побавление/удаление продукта ------------------------*/
products_ul = document.getElementById("products_filters");

function addProduct(element){
    prod_name = element.previousElementSibling.value;
    if(prod_name){
        products_ul.innerHTML += `
            <li class="menu__item">
                <input type="hidden" name="product" value="${prod_name}" checked >
                ${prod_name}
                <button class="delete_cross" onclick="deleteProduct(this)" type="button"></button>
            </li>`;
    }
    element.previousElementSibling.value = "";
}

function deleteProduct(element){
 element.parentElement.parentElement.removeChild(element.parentElement);
}

/*-------- Активация/деактивация подкатегорий при клике на родительскую категорию -------*/
category_ul = document.getElementById("categories_filters");

function childrenLikeParent(){
    let details = this.closest("details");
    let detailsInputsAll = details.getElementsByTagName("input");
    for(let i = 0; i < detailsInputsAll.length; i++){
        if (this.checked){
            detailsInputsAll[i].checked = true;
        }
        else{
            detailsInputsAll[i].checked = false;
        }
    }
}

allSummaryInCategoryUl = category_ul.getElementsByTagName('summary');
for(let i = 0; i < allSummaryInCategoryUl.length; i++){
    allSummaryInCategoryUl[i].getElementsByTagName('input')[0].onclick = childrenLikeParent;
}


/*----------------------- Очищение всех фильтров ------------------------*/
function resetAllFilters(element){
    allChecked = element.querySelectorAll("[checked]");
    for(let i=0; i< allChecked.length; i++){
        allChecked[i].removeAttribute("checked");
    }
    for(let i=0; i< products_ul.children.length; i++){
        products_ul.removeChild(products_ul.children[i]);
    }

}

/*----------- Блок посвященный сварачиванию/разворачиванию категорий фильтров   ----------*/
let exceptionFilter = document.getElementById("menu_exception_filter");

if(exceptionFilter){
    exceptionFilter.getElementsByClassName("filter__item")[0].onclick = closeExceptionFilter;

    function openExceptionFilter(){
        exceptionFilter.getElementsByClassName("filter-group")[0].className += " active";
        exceptionFilter.getElementsByClassName("filter__item")[0].className += " active";

        exceptionFilter.getElementsByClassName("filter__item")[0].onclick = closeExceptionFilter;
    }
    function closeExceptionFilter(){
        exceptionFilter.getElementsByClassName("filter-group")[0].className = 
        exceptionFilter.getElementsByClassName("filter-group")[0].className.replace(" active", '');
        exceptionFilter.getElementsByClassName("filter__item")[0].className = 
        exceptionFilter.getElementsByClassName("filter__item")[0].className.replace(" active", '');

        exceptionFilter.getElementsByClassName("filter__item")[0].onclick = openExceptionFilter;
    }
}
let caterogyFilter = document.getElementById("menu_category_filter");
let productFilter = document.getElementById("menu_product_filter");

caterogyFilter.getElementsByClassName("filter__item")[0].onclick = closeCaterogyFilter;
productFilter.getElementsByClassName("filter__item")[0].onclick = closeProductFilter;

function openCaterogyFilter(){
    caterogyFilter.getElementsByClassName("filter-group")[0].className += " active";
    caterogyFilter.getElementsByClassName("filter__item")[0].className += " active";

    caterogyFilter.getElementsByClassName("filter__item")[0].onclick = closeCaterogyFilter;
}
function closeCaterogyFilter(){
    caterogyFilter.getElementsByClassName("filter-group")[0].className = 
    caterogyFilter.getElementsByClassName("filter-group")[0].className.replace(" active", '');
    caterogyFilter.getElementsByClassName("filter__item")[0].className = 
    caterogyFilter.getElementsByClassName("filter__item")[0].className.replace(" active", '');

    caterogyFilter.getElementsByClassName("filter__item")[0].onclick = openCaterogyFilter;
}
function openProductFilter(){
    productFilter.getElementsByClassName("filter-group")[0].className += " active";
    productFilter.getElementsByClassName("filter__item")[0].className += " active";

    productFilter.getElementsByClassName("filter__item")[0].onclick = closeProductFilter;
}
function closeProductFilter(){
    productFilter.getElementsByClassName("filter-group")[0].className = 
    productFilter.getElementsByClassName("filter-group")[0].className.replace(" active", '');
    productFilter.getElementsByClassName("filter__item")[0].className = 
    productFilter.getElementsByClassName("filter__item")[0].className.replace(" active", '');

    productFilter.getElementsByClassName("filter__item")[0].onclick = openProductFilter;
}

/*---------------- Блок адаптива меню -----------------*/

let filtersMenu = document.getElementById("filters-menu");

function showFiltersMenu(){
    filtersMenu.className += " active";
}
 
function closeFiltersMenu() {
    filtersMenu.className = filtersMenu.className.replace(" active", '');
}

document.getElementById("close-filters-menu-btn").onclick = closeFiltersMenu;



/*------------------- Блок функций посвященный пагинации -------------------*/
function loadNextPage(filename){ 
    let loadNextPageBtn = document.getElementById("load-next-page-btn");
    let args = "page_num="+loadNextPageBtn.dataset.next_page+"&"+loadNextPageBtn.dataset.request_args;

    //Создаем функцию обработчик для догрузки карточек
    var showCarts = function(Request)
    {
        json_obj = JSON.parse(Request.response)
        var cards_wrapper = document.getElementsByClassName('cards-wrapper')[0];
        cards_wrapper.innerHTML += json_obj.cart_list;
        if(json_obj.next_page){
            loadNextPageBtn.dataset.next_page = json_obj.next_page;
        }
        else{
            loadNextPageBtn.parentElement.removeChild(loadNextPageBtn);
        }
                
    }

    SendRequest("GET",filename,args,showCarts);
}

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