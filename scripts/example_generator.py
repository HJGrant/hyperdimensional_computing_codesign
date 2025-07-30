import sys
from pathlib import Path
import argparse

import constants
import templates.example_template as example_template

netlist_suffix = ".sp"



def main(main_args):

    parser = argparse.ArgumentParser(description="Inserts the given parameters in the template SPICE netlist and stores the created netlists to the given location.")
    parser.add_argument("root", 
                        help="Path to root where the netlists should be generated",
                        type=Path)
    
    args = parser.parse_args(main_args)


    root = args.root

    temperature_sweep_list = [27, 60, 80]


    for cur_temp in temperature_sweep_list:
        generate(root, cur_temp)

def generate(root_output : Path, temperature):
    out_path = root_output / f'{constants.TEMPERATURE_PARAM}{temperature}'
    out_path.mkdir(parents=True, exist_ok=True)

    netlist_string = construct_netlist(temperature)
    with (out_path / f'exampel{netlist_suffix}').open('w') as fout:
        fout.write(netlist_string)
    

def construct_netlist(temperature):
    netlist_string = example_template.get_header(temperature)
    netlist_string += example_template.get_rest()
    return netlist_string



######################################################
# End of file to ensure it can be executed as script #
######################################################

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)


