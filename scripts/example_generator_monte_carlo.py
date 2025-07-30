import sys
from pathlib import Path
import argparse

import constants
import templates.rram_block_mc as rram_block 
import templates.sram_block_mc as sram_block

netlist_suffix = ".sp"


def main(main_args):

    parser = argparse.ArgumentParser(description="Inserts the given parameters in the template SPICE netlist and stores the created netlists to the given location.")
    parser.add_argument("root", 
                        help="Path to root where the netlists should be generated",
                        type=Path)
    
    args = parser.parse_args(main_args)


    root = args.root

    #technology = 'RRAM'

    temperature_sweep_list = [27]
    vdd_sweep_list = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]
    block_size = [8, 9, 10, 16]
    vec_dim = [1024]
    technology = ['RRAM', 'SRAM']

    for cur_vdd in vdd_sweep_list:
        for cur_temp in temperature_sweep_list:
            for curr_block_size in block_size:
                    for curr_vec_dim in vec_dim:
                        for curr_tech in technology:
                            generate(root, cur_temp, cur_vdd, curr_block_size, curr_vec_dim, curr_tech)

def generate(root_output : Path, temperature, vdd, block_size, vec_dim, tech):
    out_path = root_output / f'{constants.TECH}{tech}_{constants.TEMPERATURE_PARAM}{temperature}_{constants.VDD_PARAM}{vdd}_{constants.BLOCK_SIZE}{block_size}_{constants.VEC_DIM}{vec_dim}'
    out_path.mkdir(parents=True, exist_ok=True)

    netlist_string = construct_netlist(temperature, vdd, block_size, vec_dim, tech)
    with (out_path / f'exampel{netlist_suffix}').open('w') as fout:
        fout.write(netlist_string)
    

def construct_netlist(temperature, vdd, block_size, vec_dim, tech):
    if tech == 'RRAM':
        netlist_string = rram_block.get_header(temperature)
        netlist_string += rram_block.initial_setup(vdd)
        netlist_string += rram_block.init_array_lines(block_size, vec_dim)
    else:
        netlist_string = sram_block.get_header(temperature)
        netlist_string += sram_block.initial_setup(vdd)
        netlist_string += sram_block.init_array_lines(block_size, vec_dim)

    return netlist_string



######################################################
# End of file to ensure it can be executed as script #
######################################################

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)


