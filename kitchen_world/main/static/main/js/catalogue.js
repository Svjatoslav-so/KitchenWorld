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

function resetAllFilters(element){
    allChecked = element.querySelectorAll("[checked]");
    for(let i=0; i< allChecked.length; i++){
        allChecked[i].removeAttribute("checked");
    }
    for(let i=0; i< products_ul.children.length; i++){
        products_ul.removeChild(products_ul.children[i]);
    }

}

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


let filtersMenu = document.getElementById("filters-menu");

function showFiltersMenu(){
    filtersMenu.className += " active";
}
 
function closeFiltersMenu() {
    filtersMenu.className = filtersMenu.className.replace(" active", '');
}

document.getElementById("close-filters-menu-btn").onclick = closeFiltersMenu;