import os

cpp_file_name = "cpp_prob_adc.cpp"
output_name = "cpp_prob_adc"

# Searches for the include paths which contain pybind11.h and Python.h
include_string_command = "$(python3 -m pybind11 --includes)"

compile_string = f"g++ {cpp_file_name} -std=c++17 -O3 -shared -fPIC {include_string_command} -o {output_name}.so"

os.system(compile_string)