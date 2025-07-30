import sys
from pathlib import Path
import subprocess
import time
from collections import defaultdict

import argparse
import os
import datetime

import tqdm
from tqdm.contrib.concurrent import process_map


netlist_suffix = ".sp"
out_folder_name = Path("out")

def trim_and_merge_csv(input_path: Path):
    now = time.time()
    age_threshold = 30000  # seconds

    input_path = Path(input_path)
    trimmed_data = defaultdict(dict)  # {prefix: {"mt0": [...], "mc0": [...]}}

    for root, _, files in os.walk(input_path):
        for file in files:
            if file.lower().endswith(".csv"):
                file_path = Path(root) / file
                try:
                    file_age = now - file_path.stat().st_mtime
                    if file_age < age_threshold:
                        with file_path.open("r") as f:
                            lines = f.readlines()

                        if file.endswith(".mt0.csv"):
                            line_number = 3
                            key = "mt0"
                        else:
                            print(f"Skipped (unsupported suffix): {file_path}")
                            continue

                        if len(lines) > line_number:
                            trimmed_lines = lines[line_number:]
                            print(f"Trimmed: {file_path}")
                            
                            data_dir = input_path / "data"
                            data_dir.mkdir(parents=True, exist_ok=True)

                            # save the resulting trimmed data
                            out_file_path = data_dir /f"{file_path.parent.parent.name}.csv"
                            with out_file_path.open("w") as out_f:
                                out_f.writelines(trimmed_lines)
                            
                            print(f"Merged and saved: {out_file_path}")

                        else:
                            print(f"Skipped (too short): {file_path}")
                    else:
                        print(f"Skipped (too old): {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

def main(main_args):

    parser = argparse.ArgumentParser(description="Searches recursivly for all SPICE netlists starting from the given location(s). " +
                                     "At netlist for simulation is identified by the file ending '.sp'")
    parser.add_argument("roots", nargs="+", help="Path to roots where the netlists reside that should be simulated")
    parser.add_argument("--seq",
                        action="store_true",
                        help="Run all the simulations sequential")
    parser.add_argument("--proc_max",
                        type=int,
                        default=4,
                        help="Maximum number of parallel processes")
    
    args = parser.parse_args(main_args)


    roots = args.roots
    do_sequential = args.seq
    process_limit = args.proc_max

    start_time = datetime.datetime.today()

    files_to_simulate = list()
    for root in roots:
        # Walk the provided root folders and scan for netlists to simulate
        for r, folder_list, file_list in os.walk(root):
            #print(f"Getting Files {file_list}")
            # Skip output folders
            if "out" in folder_list:
                folder_list.remove("out")
            #print(r)
            next_root = Path(r)

            files_to_simulate += [next_root / Path(x) for x in file_list if x.endswith(netlist_suffix)]
    

    error_counter = 0
    if do_sequential:
        print("Running Sequentialy!")
        for work_item in tqdm.tqdm(files_to_simulate):
            return_code = worker(work_item)
            if return_code != 0:
                error_counter += 1

            
    else:
        print("Running in Parallel!")
        return_codes = process_map(worker, files_to_simulate, max_workers=process_limit, chunksize=process_limit)
        error_counter = sum([0 if x == 0 else 1 for x in return_codes])

            
    trim_and_merge_csv(root)

    print()
    print("Done")
    print(f"Errors: {error_counter}")
    print("Time elapsed: {}".format(datetime.datetime.today() - start_time))

def worker(simulation_file : Path):
    out_path = simulation_file.parent / out_folder_name 
        
    hspice_call_args_list = ["hspice", "-i", str(simulation_file), "-o", str(out_path) + '/']

    return_code = 0
    return_code = subprocess.call(hspice_call_args_list, stdout=subprocess.DEVNULL)
    if return_code != 0:
        print("#########")
        print("Error of call: {}".format(hspice_call_args_list))
        print("Returned: '{}'".format(return_code))
        print("#########")
    return return_code

######################################################
# End of file to ensure it can be executed as script #
######################################################

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)



