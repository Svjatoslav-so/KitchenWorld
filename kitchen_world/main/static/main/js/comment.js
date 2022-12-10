let form = document.getElementById("sent_comment")
let div_reply = document.getElementById("comment-reply-message")

function show(){
    for (let input of document.getElementsByName("parent_comment_id")){
        form.removeChild(input)
    }
    answer_input = document.createElement("input")
    answer_input.setAttribute("type","hidden")
    answer_input.setAttribute("name","parent_comment_id")
    answer_input.setAttribute("value",this.id)
    form.appendChild(answer_input)

    comment = this.closest(".recipe-comment__head")

    for(let i=div_reply.children.length-2; i>0; i--){
        div_reply.removeChild(div_reply.children[i])
    }
    div_reply.insertBefore(comment.firstElementChild.firstElementChild.cloneNode(true), div_reply.lastElementChild)
    div_reply.insertBefore(comment.parentNode.lastElementChild.cloneNode(true), div_reply.lastElementChild)
    div_reply.classList.remove("hide")
    div_reply.classList.add("show")
    

}

let answer_btns = document.getElementsByName("answer_comment_btn")
for(let btn of answer_btns){
    btn.onclick = show
}

cancel_btn = document.getElementById("cancel_btn")
if(cancel_btn){
    cancel_btn.onclick = function(){
        div_reply.classList.remove("show")
        div_reply.classList.add("hide")
        for (let input of document.getElementsByName("parent_comment_id")){
            form.removeChild(input)
        }
    }
}



