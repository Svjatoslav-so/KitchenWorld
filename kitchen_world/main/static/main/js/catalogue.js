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