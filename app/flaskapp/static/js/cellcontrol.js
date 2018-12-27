// cellcontrol.js holds all the functionality for the cellcontrol.html view

function run_cell(cell_id) {
    num_cycles = document.getElementById('num_cycles_' + cell_id).value;
    cycle_id = document.getElementById("cycle_select_" + cell_id).selectedIndex;

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.status == 200) {
                param_list = this.responseText.split(',');

                param_vals = [];
                for(pid = 0; pid < param_list.length; pid++){
                    pdocindex = param_list[pid] + "_" + cell_id;
                    param_vals.push(document.getElementById(pdocindex).value);
                }

                form_string = "cell_id=" + cell_id + "&num_cycles=" + num_cycles + "&cycle_id=" + cycle_id;

                for(pid = 0; pid < param_list.length; pid++){
                    form_string = form_string + "&" + param_list[pid] + "=" + param_vals[pid];
                }

                var xhttp2 = new XMLHttpRequest();
                xhttp2.onreadystatechange = function() {
                    if (this.readyState == 4) {
                        if (this.status == 200) {
                            document.getElementById("cellbox_" + cell_id).innerHTML = this.responseText;
                        } else{
                            alert(this.status);
                        }
                    }
                };
                xhttp2.open("POST", "/run_cell", true);
                xhttp2.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
                xhttp2.send(form_string);

            } else{
                alert(this.status);
            }
        }
    };
    xhttp.open("POST", "/get_cycle_param_names", true);
    xhttp.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    xhttp.send("cycle_id=" + cycle_id);
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