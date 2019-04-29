import csv, glob, os, json, base64
from .cycle import Cycle

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
SITE_ROOT = os.path.join(SITE_ROOT, '../../')
CYCLES_URL = os.path.join(SITE_ROOT, "files/cycles")

class CycleBank:

    CYCLE_INFO = []

    def __init__(self):
        with open(os.path.join(CYCLES_URL, 'cycles.json')) as f:
            self.CYCLE_INFO = json.load(f)

    # This processes a newly uploaded .cycle file and adds it to the database
    def process_cycle_file(self, filename):
        cycle_info = self.get_cycle_info(os.path.join(CYCLES_URL, filename))

        cycle_entry = {
            'name': cycle_info[0],
            'file': filename,
            'parameters': cycle_info[1]
        }

        self.CYCLE_INFO.append(cycle_entry)

        database_filename = os.path.join(CYCLES_URL, 'cycles.json')
        os.remove(database_filename)

        with open(os.path.join(CYCLES_URL, 'cycles.json'), 'w') as f:
            f.writelines(json.dumps(self.CYCLE_INFO, sort_keys=True, indent=2))

    # This gets the file and display names of all the .cycle files in files/cycles
    def get_all_cycle_info(self):
        all_cycle_files = glob.glob('../files/cycles/*.cycle')
        all_cycle_info = []
        for fid in range(len(all_cycle_files)):
            file = all_cycle_files[fid]
            cycle_info = self.get_cycle_info(file)
            all_cycle_info.append({
                'filename': file,
                'displayname': cycle_info[0],
                'parameters': cycle_info[1]
            })

        return all_cycle_info

    # This gets the info of a single .cycle file, including the parameters it needs and it's display name
    def get_cycle_info(self, filename):
        with open(filename, 'r') as f:
            reader = csv.reader(f)

            parameter_names = []

            line1 = reader.__next__()
            display_name = line1[0]

            line2 = reader.__next__()
            if line2[0] == "Parameter Names:":
                # Here we need to define the local parameter variables which will hold inputs,
                # then check that we have the right amount of inputs
                for col in range(len(line2)):
                    if not col == 0:
                        parameter_names.append(line2[col])

            return [display_name, parameter_names]


# This turns the cycle_file into a list of commands and parameters bound to the correct objects
def load_cycle(cell, filename, parameters):
    cycle_info = parse_cycle_file(filename, parameters)
    cycle = Cycle(cycle_info, cell)
    return cycle


# This parses a cycle file
def parse_cycle_file(filename, parameters):
    calls = []
    call_args = []
    parameter_dict = {}

    # First, fill out our dictionary
    with open(os.path.join(CYCLES_URL, filename), 'r') as f:
        reader = csv.reader(f)

        parameter_names = []

        line1 = reader.__next__()  # Skip the first line, it's just the display name of the cycle
        line2 = reader.__next__()
        if line2[0].startswith("Parameter"):
            # Here we need to define the local parameter variables which will hold inputs,
            # then check that we have the right amount of inputs
            for col in range(len(line2)):
                if not col == 0:
                    parameter_names.append(line2[col])

            if not len(parameter_names) == len(parameters):
                ValueError("Parameter number mismatch! len(parameters) must equal len(parameter_names)")

            for iid in range(len(parameter_names)):
                parameter_dict[parameter_names[iid]] = parameters[iid]

    # Then, list all the command along with the arguments they take (wrt. dict), and continue to fill out dict as needed
    with open(os.path.join(CYCLES_URL, filename), 'r') as f:
        reader = csv.reader(f)

        line1 = reader.__next__()  # Skip the first line, it's just the display name of the cycle
        for row in reader:
            if row[0] is not "Parameter Names:":
                calls.append(row[0])
                rowparse = parse_row_params(row, parameter_dict)
                parameter_dict = rowparse['dict']
                call_args.append(rowparse['args'])

    cycle_commands = {
        'call_names': calls,
        'call_args': call_args,
        'arg_dictionary': parameter_dict
    }

    return cycle_commands


def parse_row_params(rowvec, parameter_dict):
    a = []

    # If we have no parameters, return an empty array.
    if len(rowvec) < 2:
        return {
            'dict': parameter_dict,
            'args': ''
        }

    # If we only have one parameter, just return that parameter
    if len(rowvec) is 2:
        if not len(parameter_dict) == 0 and rowvec[1] in parameter_dict:
            a = rowvec[1]
        else:
            name = base64.b32encode(rowvec[1].encode())
            a = name
            parameter_dict[name] = rowvec[1]

        return {
            'dict': parameter_dict,
            'args': a
        }

    iid = 1
    while iid is not len(rowvec):
        if not len(parameter_dict) == 0 and rowvec[iid] in parameter_dict:
            a.append(rowvec[iid])
        else:
            name = base64.b32encode(rowvec[iid].encode())
            a.append(name)
            parameter_dict[name] = rowvec[iid]

        iid = iid + 1

    return {
        'dict': parameter_dict,
        'args': a
    }
