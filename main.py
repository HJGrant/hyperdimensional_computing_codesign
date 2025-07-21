import numpy as np
import os
import sys
import csv
from tqdm import tqdm


from error_injection import cpp_prob_adc

base_path = "/home/woss/Documents/final_task/final_project_bic/4_gram/"
languages = ["eng", "deu", "fra", "swe", "ita", "spa", "por", "pol", "nld", "dan"]
csv_file_path = 'results.csv'
npy_file_path = '/home/woss/Documents/final_task/final_project_bic/compute_conf_matrices/conf_matrix_results.npy'

#dimensions = [128]  # Example dimensions
#block_sizes = [2]   # Example block sizes
#precisions = [1]          # Example precisions
dimensions = [128, 256, 512, 1024, 2048, 4096]  # Example dimensions
block_sizes = [8, 9, 10, 11, 12, 13, 14, 15, 16]   # Example block sizes
precisions = [1, 2, 3, 4, 5, 6, 7, 8]          # Example precisions


adc_model_matrix = [
    [1, 0, 0, 0, 0],  
    [0, 1, 0, 0, 0],  
    [0, 0, 1, 0, 0],  
    [0, 0, 0, 1, 0], 
    [0, 0, 0, 0, 1],  
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


def run_inference(class_vectors, test_vectors, number_of_samples, block_size, precision, adc_model_matrix):
    results = cpp_prob_adc.inference_with_errors(
        class_vectors,
        test_vectors,
        number_of_samples,
        block_size,
        precision,
        adc_model_matrix
    )
    return results


def generate_test_paths(dimension):
    file_paths = [f"{base_path}dimension_{dimension}/{lang}.txt" for lang in languages]
    return file_paths

def get_class_path(dimension):
    return f"{base_path}dimension_{dimension}/training_language.txt"

def generate_adc_model_matrix(precision):
    # Create an identity matrix with precision + 1 rows and columns
    return np.eye(precision + 1)

def create_csv_file(csv_file_path, all_results):
    # Write the results to a CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['Dimension', 'Block Size', 'Precision', 'Results'])
        # Write the data
        for result in all_results:
            writer.writerow([result['dimension'], result['block_size'], result['precision'], result['results']])



def run_npy_data():
    data = np.load(npy_file_path, allow_pickle=True)
    updated_data = []

    for entry in tqdm(data):
        dimension = entry['vec_dim']
        number_of_samples = 100  # Replace this if it's stored somewhere
        block_size = entry['block_size']
        precision = entry['precision']
        adc_model_matrix = entry['conf_matrix'] # Or fetch from elsewhere if needed

        if dimension in [1024, 2048] and block_size in [8, 16] and precision < block_size:
            test_paths = generate_test_paths(dimension)
            results = []
            for path in test_paths:
                result = run_inference(
                    import_dict_from_txt(get_class_path(dimension)),
                    import_dict_from_txt(path),
                    number_of_samples,
                    block_size,
                    precision,
                    adc_model_matrix
                )
                results.append(result)
            average = np.mean(results)
            entry['inference_result'] = average
            updated_data.append(entry)
            print(entry)
            np.save(f'conf_matrix_results/inference_results.npy', updated_data)

def main():

    run_npy_data()    




    


if __name__ == "__main__":
    results = main()
    print("results:")
    print(results)

    #result_pol = run_inference(import_dict_from_txt("/home/woss/Documents/final_task/final_project_bic/4_gram/dimension_256/training_language.txt"), import_dict_from_txt("/home/woss/Documents/final_task/final_project_bic/4_gram/dimension_256/swe.txt"), 1, 20, 4, adc_model_matrix)
    #print("result_pol:")
    #print(result_pol)




"""
def oldstuff()
        all_results = []

    # Iterate over each combination of parameters
    for dimension in dimensions:
        for block_size in block_sizes:
            for precision in precisions:
                # Generate the adc_model_matrix based on the precision
                adc_model_matrix = generate_adc_model_matrix(precision)
                print(adc_model_matrix)
                # Generate test paths for the current dimension
                test_paths = generate_test_paths(dimension)

                # Initialize a list to store results for the current parameter combination
                results = []

                # Run inference for each path
                for path in test_paths:
                    result = run_inference(
                        import_dict_from_txt(get_class_path(dimension)),
                        import_dict_from_txt(path),
                        1,
                        block_size,
                        precision,
                        adc_model_matrix
                    )
                    results.append(result)

                # Calculate the average for the current parameter combination
                average = np.mean(results, axis=0)
                #print(average)
                #results.append(average)

                # Store the results along with the parameters
                all_results.append({
                    'dimension': dimension,
                    'block_size': block_size,
                    'precision': precision,
                    'results': float(average)
                })
    
    create_csv_file(csv_file_path, all_results)
    """
    