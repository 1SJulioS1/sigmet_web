$('#tabla_modal').dataTable({
    // // "order": true,
    // // "info": true,
    // "search": {
    //     "smart": false
    // },
    // // "paging": true,
    // // "displayStart":20,
    // // "orderClasses": false
    // "pagingType": "full_numbers"
});

var modal = document.getElementById("modal_gen");

// Get the button that opens the modal
var btn_uso = document.getElementById("btn_uso");

var btn_alm = document.getElementById("btn_alm");

var btn_roto = document.getElementById("btn_roto");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

var tabla = document.getElementById('tabla_modal');

function limpiar_body() {
    tabla.removeChild(tabla.lastElementChild);
}

function rellenar_tabla(d) {
    limpiar_body();
    let body = document.createElement('tbody');
    for (let key in d) {
        let tr = document.createElement('tr');
        let td1 = document.createElement('td');
        let emp = document.createTextNode(key + '');
        td1.appendChild(emp);
        tr.appendChild(td1);
        let td2 = document.createElement('td');
        let inst = document.createTextNode(d[key] + '');
        td2.appendChild(inst);
        tr.appendChild(td2);
        body.appendChild(tr);
    }
    tabla.appendChild(body);
}

// When the user clicks the button, open the modal
function modal_function(inst) {
    let d = JSON.parse(inst);
    rellenar_tabla(d);
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    modal.style.display = "none";
};
// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};




