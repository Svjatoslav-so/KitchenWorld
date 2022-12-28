
// event.type должен быть keypress
function getChar(event) {
    if (event.which == null) {
    if (event.keyCode < 32) return null;
    return String.fromCharCode(event.keyCode) // IE
    }

    if (event.which != 0 && event.charCode != 0) {
    if (event.which < 32) return null;
    return String.fromCharCode(event.which) // остальные
    }

    return null; // специальная клавиша
}

var ingredientsForm = document.forms.ingredients;

var ingredients = ingredientsForm.querySelectorAll("[data-original_quantity]");

for(var i = 0; i < ingredients.length; i++){
    ingredients[i].onkeypress = function(e) {
        e = e || event;
        var chr = getChar(e);

        if (e.ctrlKey || e.altKey || chr == null) return; // специальная клавиша
        if (chr < '0' || chr > '9') return false;
    }

    ingredients[i].onfocus = toSi;

    // клавиатура, вставить/вырезать клавиатурой
    ingredients[i].onkeyup = calculate;

    // любые действия, кроме IE. В IE9 также работает, кроме удаления
    ingredients[i].oninput = calculate;

    ingredients[i].onchange = fixDimension;
    ingredients[i].onblur = fixDimension;

    ingredients[i].onpropertychange = function() { // для IE8- изменение значения, кроме удаления
        event.propertyName == "value" && calculate();
    }
}
// console.log("Ingredients ",ingredients);

function get_dimension(element){
    let dimension = 1;
    let option = element.nextElementSibling.firstElementChild;
    // console.log(option);
    if(option && +option.value){
        dimension = +option.value;
    }
    return dimension;
}

function isShtuky(element, name){
    let option = element.nextElementSibling.querySelector(`[name="${name}"]`);
    return option ? option.getAttribute("name") == name: false;
}

function addOption(element, value, showValue){
    let newOption = element.nextElementSibling.querySelector(`[name="${showValue}"]`);
    if(newOption){
        newOption.selected = true;
    }
    else{
        let newOption = document.createElement("option");
        newOption.value = value;
        newOption.text = showValue;
        newOption.setAttribute("name",showValue);
        newOption.selected = true;
        element.nextElementSibling.appendChild(newOption);
    }
    allOption = element.nextElementSibling.children;
        for(let i = 0; i<allOption.length; i++){
            if(allOption[i] != newOption){
                element.nextElementSibling.remove(allOption[i]);
            }
        }
}

function toSi(){
    // console.log("toSi");
    for(var i = 2; i < ingredients.length; i++){
        if(isShtuky(ingredients[i], "л")){
            ingredients[i].value = +ingredients[i].value*1000;
            addOption(ingredients[i], "ML", "мл");
        }
        else if(isShtuky(ingredients[i], "кг")){
            ingredients[i].value = +ingredients[i].value*1000;
            addOption(ingredients[i], "G", "г");
        }
    }
}

function calculate(event) {
    // console.log("Event: ", event);
    // if((+event.key >= 0 && +event.key < 10) || event.key == "v" || event.key == "V"){
    if(event.key != "Enter"){
        // console.log("Value :", this.value);
        // console.log("Dimension", get_dimension(this));
        // console.log("Data :", this.dataset.original_quantity);
        let k = (+this.value)*get_dimension(this)/(+this.dataset.original_quantity);
        // console.log("K :", k);

        for(var i = 0; i < ingredients.length; i++){
            if(ingredients[i] != this){
                let newValue = k * (+ingredients[i].getAttribute("data-original_quantity"));
                // console.log("V ", i, " :", newValue, ingredients[i].getAttribute("data-original_quantity"));
                ingredients[i].value = newValue;
            }
        }
    }
    else{
        fixDimension();
    }
}

function fixDimension(){
    // console.log("FIX");
    for(var i = 0; i < ingredients.length; i++){
        if(i == 0){
            let roundValue = Math.round(+ingredients[i].value);
            ingredients[i].value = roundValue > 0 ? roundValue : 1;
        }
        if(i>1){
            let rowValue = +ingredients[i].value*get_dimension(ingredients[i]) 
            if(isShtuky(ingredients[i], "шт")){
                let roundValue = Math.round(+ingredients[i].value);
                // console.log("SHUKY");
                ingredients[i].value = roundValue > 0 ? roundValue : 1;
            }
            else if(rowValue/1000 >= 1){
                // console.log("SECOND");
                if(isShtuky(ingredients[i], "мл")){
                    addOption(ingredients[i], 1000, "л");
                }
                else if(isShtuky(ingredients[i], "г")){
                    addOption(ingredients[i], 1000, "кг");
                }
                ingredients[i].value = rowValue/1000;
            }
            else{
                // console.log("ELSE");
                if(isShtuky(ingredients[i], "л")){
                    // console.log("liters");
                    addOption(ingredients[i], "ML", "мл");
                }else if(isShtuky(ingredients[i], "кг")){
                    // console.log("grams");
                    addOption(ingredients[i], "G", "г");
                }
            }
        }
    
    }

}