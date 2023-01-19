const btnsConfirm = document.querySelectorAll("#btnBorrar")

if (btnsConfirm.length) {
    for (const btn of btnsConfirm) {
        btn.addEventListener("click", event => {
            resp = confirm("Esta opción no tiene marcha atrás, ¿Confirma?")
            if(!resp) event.preventDefault()
        })
    }
}