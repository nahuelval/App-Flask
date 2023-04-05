const btnsConfirm = document.querySelectorAll("#btnBorrar")
const btnToggle = document.querySelector("#navbarNavAltMarkup")
const btnNavBar = document.querySelector(".navbar-toggler")

if (btnsConfirm.length) {
    for (const btn of btnsConfirm) {
        btn.addEventListener("click", event => {
            resp = confirm("Esta opción no tiene marcha atrás, ¿Confirma?")
            if(!resp) event.preventDefault()
        })
    }
}

btnNavBar.addEventListener('click', function(){
    console.log("a")
    if(btnToggle.className == "collapse navbar-collapse")
        btnToggle.className = "navbar-collapse"
    else
        btnToggle.className = "collapse navbar-collapse"
})