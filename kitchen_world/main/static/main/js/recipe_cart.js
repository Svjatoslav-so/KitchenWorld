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
            let argsList = r_args.split("&")
            let type = argsList[0].split("=")[1]
            let currentPage = argsList[2].split("=")[1]
            r_handler(Request, type, currentPage);
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
        
        //Посылаем нуль-запрос
        Request.send(null);
    }
} 


function Like(filename, elementName,myProfileCurrentPage)
{
    //Создаем функцию обработчик для установки лайка
    var On = function(Request, type, myProfileCurrentPage)
    {
        console.log("On");  
        console.log(Request.responseText);
        if(Request.responseText != "OK"){
            // var html = document.getElementsByTagName('html')[0];
            // html.innerHTML = Request.responseText;
            location.reload();
        }
        else{
            let elems = document.getElementsByName(elementName)
            elems.forEach(element => {
                // element.innerHTML = Request.responseText;
                element.firstElementChild.className += " active";
                // console.log(element.lastElementChild);
                // console.log(element.lastElementChild.innerHTML);
                element.lastElementChild.innerHTML = parseInt(element.lastElementChild.innerHTML)+1;
                // console.log(element.lastElementChild.innerHTML);
                element.onclick = function(){
                    Like('/stars_off/', elementName);
                }
                // console.log("onclick: ", element.onclick);
            }); 
        }

    }

     //Создаем функцию обработчик для удаления лайка
     var Off = function(Request, type, myProfileCurrentPage)
     {
        console.log("Off");  
        console.log(Request.responseText);
        if(Request.responseText != "OK"){
            // var html = document.getElementsByTagName('html')[0];
            // html.innerHTML = Request.responseText;
            location.reload();
        }
        else{
            let elems = document.getElementsByName(elementName);
            elems.forEach(element => {
                // element.innerHTML = Request.responseText;
                element.firstElementChild.className = element.firstElementChild.className.replace('active', '');
                //  console.log(element.lastElementChild);
                //  console.log(element.lastElementChild.innerHTML);
                element.lastElementChild.innerHTML = parseInt(element.lastElementChild.innerHTML)-1;
                //  console.log(element.lastElementChild.innerHTML);
                element.onclick = function(){
                    Like('/stars_on/', elementName);
                }
                //  console.log("onclick: ", element.onclick);
                if(type=="B" && myProfileCurrentPage=="Закладки"){
                    element.closest(".card").style.display="none" 
                }
                if(type=="L" && myProfileCurrentPage=="Понравившиеся"){
                    element.closest(".card").style.display="none" 
                }

            }); 
        }
 
     }
     let values = elementName.split("_")
     console.log(values)
     let args = `type=${values[0]}&id=${values[1]}&currentPage=${myProfileCurrentPage}`
    
    //Отправляем запрос
    if(filename == '/stars_off/'){
        SendRequest("GET",filename,args,Off);
    }
    else{
        SendRequest("GET",filename,args,On);
    }
    
} 
