// cellcontrol.js holds all the functionality for the cellcontrol.html view

function run_cell(cell_id) {
    num_cycles = document.getElementById('num_cycles_' + cell_id).value;

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.response === true) {
                alert('Running Cell #' + cell_id + " for " + num_cycles +  " cycles");
                window.location.reload(true);
            } else {
                alert("Failed!");
            }

        }
    };
    xhttp.open("POST", "/cellcontrol");
    xhttp.setRequestHeader("cell_id", cell_id);
    xhttp.setRequestHeader("num_cycles", num_cycles);
    xhttp.send()
}