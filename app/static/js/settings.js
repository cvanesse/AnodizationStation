function clear_logs(){
    // Asynchronously tell the server to start the cell, then update the cellbox
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.status == 200) {
                if (this.responseText == "Success") {
                    setwaiting(cell_id);
                    setTimeout(render_cellbox(cell_id), 15);
                } else {
                    alert(this.responseText);
                    setTimeout(render_cellbox(cell_id), 15);
                }
            }
        }
    };
    xhttp.open("POST", "/clear_logs", true);
    xhttp.setRequestHeader('content-type', 'application/json; charset=UTF-8');
}

function clear_cycles(){
    // Asynchronously tell the server to start the cell, then update the cellbox
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.status == 200) {
                if (this.responseText == "Success") {
                    setwaiting(cell_id);
                    setTimeout(render_cellbox(cell_id), 15);
                } else {
                    alert(this.responseText);
                    setTimeout(render_cellbox(cell_id), 15);
                }
            }
        }
    };
    xhttp.open("POST", "/clear_cycles", true);
    xhttp.setRequestHeader('content-type', 'application/json; charset=UTF-8');
}