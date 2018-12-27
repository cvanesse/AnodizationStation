// cellcontrol.js holds all the functionality for the cellcontrol.html view

function run_cell(cell_id) {
    num_cycles = document.getElementById('num_cycles_' + cell_id).value;

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.status == 200) {
                alert(this.responseText);
            } else{
                alert(this.status);
            }
        }
    };
    xhttp.open("POST", "/run_cell", true);
    xhttp.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    xhttp.send("cell_id=" + cell_id + "&num_cycles=" + num_cycles);
}