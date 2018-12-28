function init() {
    // Then, we render all of the cells (which is done asynchronously)
    for (cid = 0; cid < window.CELL_CONFIG.length; cid++) {
        setwaiting(cid);
        render_cellbox(cid)
    }
}

function run_cell(cell_id) {
    var info = {
        "num_cycles": parseInt(document.getElementById("num_cycles_" + cell_id).value),
        "cell_id": cell_id,
        "cycle_id": document.getElementById("cycle_select_" + cell_id).selectedIndex,
        "cycle_params": []
    };

    for (pid = 0; pid < window.CYCLE_INFO[info.cycle_id].parameters.length; pid++) {
        pname = window.CYCLE_INFO[info.cycle_id].parameters[pid];
        info["cycle_params"].push(document.getElementById(pname + "_" + cell_id).value);
    }

    // Asynchronously tell the server to start the cell, then update the cellbox
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.status == 200) {
                if (this.responseText == "Cell started.") {
                    setrunning(cell_id);
                    setTimeout(render_cellbox(cell_id), 15);
                } else {
                    setwaiting(cell_id);
                    setTimeout(render_cellbox(cell_id), 15);
                }
            }
        }
    };
    xhttp.open("POST", "/run_cell", true);
    xhttp.setRequestHeader('content-type', 'application/json; charset=UTF-8');
    xhttp.send(JSON.stringify(info));
}

function render_cellbox(cell_id) {
    // Asynchronously fetch the rendered HTML for this cell_id
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.status == 200) {
                document.getElementById("cellbox_" + cell_id).innerHTML = this.responseText;
                status_text = document.getElementById("status_" + cell_id).innerText;
                if (status_text == "Waiting...") {
                    setwaiting(cell_id)
                    render_cycle_parameters(0, cell_id);
                } else {
                    setTimeout(function() {
                        render_cellbox(cell_id);
                    }, 5000)
                }
            }
        }
    };
    xhttp.open("POST", "/render", true);
    xhttp.setRequestHeader('content-type', 'application/json; charset=UTF-8');
    xhttp.send(JSON.stringify({"name": "cellbox", "cell_id": cell_id}));
}

function render_cycle_parameters(cycle_id, cell_id) {
    // Asynchronously fetch the rendered HTML for this cell_id
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.status == 200) {
                document.getElementById("cycleparams_" + cell_id).innerHTML = this.responseText;
                document.getElementById("cycle_select_" + cell_id).selectedIndex = cycle_id;
            }
        }
    };
    xhttp.open("POST", "/render", true);
    xhttp.setRequestHeader('content-type', 'application/json; charset=UTF-8');
    xhttp.send(JSON.stringify({"name": "cycleparams", "cell_id": cell_id, "cycle_id": cycle_id}));
}

function update_cycle_parameters(cell_id) {
    cycle_id = document.getElementById("cycle_select_" + cell_id).selectedIndex;
    render_cycle_parameters(cycle_id, cell_id);
}

function setrunning(cell_id) {
    window.RUNNING[cell_id] = true;
}

function setwaiting(cell_id) {
    window.RUNNING[cell_id] = false;
}