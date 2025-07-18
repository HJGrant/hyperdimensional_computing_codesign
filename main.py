import numpy as np
import os
import sys

from error_injection import cpp_prob_adc

file_path = "test.txt"

class_path = "training_language.txt"

adc_model_matrix = [
    [0.9, 0.1, 0.0, 0.0, 0.0],  # True HD = 0: mostly stays 0, small chance for 1
    [0.1, 0.7, 0.2, 0.0, 0.0],  # True HD = 1
    [0.05, 0.15, 0.7, 0.1, 0.0],  # True HD = 2
    [0.02, 0.08, 0.2, 0.6, 0.1],  # True HD = 3
    [0.01, 0.04, 0.15, 0.3, 0.5],  # True HD = 4
]


def import_dict_from_txt(file_path):
    with open(file_path, 'r') as file:
        print(file_path)
        vectors = []
        for line in file:
            parts = line.strip().split(":")
            label = parts[0].strip()
            bit_values = parts[1].strip().split()
            bit_string = ''.join(bit_values)

            vectors.append((label, bit_string))          
    return vectors


def main():

    class_vectors = import_dict_from_txt(file_path)
    test_vectors = import_dict_from_txt(file_path)
    number_of_samples = 5
    block_size = 10
    precision = 4

    print(type(class_vectors), type(class_vectors[0]), type(class_vectors[0][0]), type(class_vectors[0][1]))
    print(type(adc_model_matrix), type(adc_model_matrix[0]), type(adc_model_matrix[0][0]))
 
    results = cpp_prob_adc.inference_with_errors(
        class_vectors,
        test_vectors,
        number_of_samples,
        block_size,
        precision,
        adc_model_matrix
    )
    return results
    
if __name__ == "__main__":
    results = main()

    print("results:")
    print(results)