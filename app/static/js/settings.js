function clear_logs(){
    // Asynchronously tell the server to start the cell, then update the cellbox
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.status == 200) {
                if (this.responseText == "Success") {
                    alert("Logs Cleared!")
                } else {
                    alert(this.responseText);
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
                    alert("Cycles Cleared!")
                } else {
                    alert(this.responseText);
                }
            }
        }
    };
    xhttp.open("POST", "/clear_cycles", true);
    xhttp.setRequestHeader('content-type', 'application/json; charset=UTF-8');
}