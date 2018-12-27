// cellcontrol.js holds all the functionality for the cellcontrol.html view

function run_cell(cell_id) {
    num_cycles = document.getElementById('num_cycles_' + cell_id).value;

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.status == 200) {
                document.getElementById("cellbox_" + cell_id).innerHTML = this.responseText;
            } else{
                alert(this.status);
            }
        }
    };
    xhttp.open("POST", "/run_cell", true);
    xhttp.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    xhttp.send("cell_id=" + cell_id + "&num_cycles=" + num_cycles);
}

function update_cellbox(cell_id) {
    cycle_id = document.getElementById("cycle_select_" + cell_id).selectedIndex;

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.status == 200) {
                document.getElementById("cycleparams_" + cell_id).innerHTML = this.responseText;
            } else{
                alert(this.status);
            }
        }
    };
    xhttp.open("POST", "/get_cycle_param_display", true);
    xhttp.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    xhttp.send("cycle_id=" + cycle_id + "&cell_id=" + cell_id);
}