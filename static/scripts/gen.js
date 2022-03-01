

var modal = document.getElementById("modal_gen");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

var tabla = document.getElementById('tabla_modal');

function limpiar_body(t) {
    t.removeChild(t.lastElementChild);
}

function rellenar_tabla(t, d) {
    limpiar_body(t);
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
    t.appendChild(body);
}

// When the user clicks the button, open the modal
function modal_function(inst) {
    let div = document.getElementById("div_tabla");
    div.removeChild(div.lastElementChild);
    let t = document.createElement("table");
    t.setAttribute("id", "tabla_modal");
    let thead = document.createElement("thead");
    let tr = document.createElement("tr");
    let th1 = document.createElement("th");
    let th2 = document.createElement("th");
    let text1 = document.createTextNode("Empresas");
    let text2 = document.createTextNode("Instrumentos");
    let body = document.createElement("tbody");
    th1.appendChild(text1);
    th2.appendChild(text2);
    tr.appendChild(th1);
    tr.appendChild(th2);
    thead.appendChild(tr);
    t.appendChild(thead);
    t.appendChild(body);
    div.appendChild(t)
    let d = JSON.parse(inst);
    rellenar_tabla(t, d);
    $('#tabla_modal').DataTable({});
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




