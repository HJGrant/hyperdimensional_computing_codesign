import numpy as np
import string
import os
from tqdm import tqdm
import multiprocessing
import sys
from scipy.spatial import distance

#import functions as fn

#constants
dimensions = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
gram_size = 4
#iterator = 50
#bic_training_file_array = {'dan': '/space/chair-nas/teaching/bic_lab/initial_material/hdc/language_recognition_dataset/training/dan.txt'}
bic_training_file_array = {
    'dan': '/space/chair-nas/teaching/bic_lab/initial_material/hdc/language_recognition_dataset/training/dan.txt',
    'deu': '/space/chair-nas/teaching/bic_lab/initial_material/hdc/language_recognition_dataset/training/deu.txt',
    'eng': '/space/chair-nas/teaching/bic_lab/initial_material/hdc/language_recognition_dataset/training/eng.txt',
    'fra': '/space/chair-nas/teaching/bic_lab/initial_material/hdc/language_recognition_dataset/training/fra.txt',
    'ita': '/space/chair-nas/teaching/bic_lab/initial_material/hdc/language_recognition_dataset/training/ita.txt',
    'nld': '/space/chair-nas/teaching/bic_lab/initial_material/hdc/language_recognition_dataset/training/nld.txt',
    'pol': '/space/chair-nas/teaching/bic_lab/initial_material/hdc/language_recognition_dataset/training/pol.txt',
    'por': '/space/chair-nas/teaching/bic_lab/initial_material/hdc/language_recognition_dataset/training/por.txt',
    'spa': '/space/chair-nas/teaching/bic_lab/initial_material/hdc/language_recognition_dataset/training/spa.txt',
    'swe': '/space/chair-nas/teaching/bic_lab/initial_material/hdc/language_recognition_dataset/training/swe.txt'
}

bic_testing_file_array = {
    'dan': '/space/chair-nas/teaching/bic_lab/initial_material/hdc/language_recognition_dataset/testing/dan.txt',
    'deu': '/space/chair-nas/teaching/bic_lab/initial_material/hdc/language_recognition_dataset/testing/deu.txt',
    'eng': '/space/chair-nas/teaching/bic_lab/initial_material/hdc/language_recognition_dataset/testing/eng.txt',
    'fra': '/space/chair-nas/teaching/bic_lab/initial_material/hdc/language_recognition_dataset/testing/fra.txt',
    'ita': '/space/chair-nas/teaching/bic_lab/initial_material/hdc/language_recognition_dataset/testing/ita.txt',
    'nld': '/space/chair-nas/teaching/bic_lab/initial_material/hdc/language_recognition_dataset/testing/nld.txt',
    'pol': '/space/chair-nas/teaching/bic_lab/initial_material/hdc/language_recognition_dataset/testing/pol.txt',
    'por': '/space/chair-nas/teaching/bic_lab/initial_material/hdc/language_recognition_dataset/testing/por.txt',
    'spa': '/space/chair-nas/teaching/bic_lab/initial_material/hdc/language_recognition_dataset/testing/spa.txt',
    'swe': '/space/chair-nas/teaching/bic_lab/initial_material/hdc/language_recognition_dataset/testing/swe.txt'
}


base_directory = '/home/woss/Documents/final_task/final_project_bic/4_gram'


#initialise characterlist
characters = list(string.ascii_lowercase + string.digits + string.punctuation + ' ' + '')
characters.remove(':')

#matrix for n grams
matrix = []

#functions:
def get_vector(input_data):
    # Check if input_data is a NumPy array, if so return it, otherwise lookup in char_hypervectors
    try:
        return input_data if isinstance(input_data, np.ndarray) else char_hypervectors[input_data]
    except Exception as e:
        print(f"input_data: {input_data} and error {e}")

def return_nparray(input_data, vector):
    array = vector[input_data]
    np_array = np.array(array)
    #print(f"input = {input_data}, array = {array}, np_array = {np_array}, vector = {vector}")
    return np_array

#shift function accepts a vector and a dictionary element as input
def shift(input_data):
        #return np.roll(get_vector(input_data),1)
        return np.roll(input_data, 1)

#multiply input function accepts two vectors or dictionary elements or a mix as input
def xor(input_data1, input_data2):
    #vector1 = get_vector(input_data1)
    #vector2 = get_vector(input_data2)
    vector1 = input_data1
    vector2 = input_data2
    return np.bitwise_xor(vector1, vector2)

def create_4_gram(char1, char2, char3, char4):
    vector = xor(char1, shift(char2))
    vector = xor(vector, shift(shift(char3)))
    vector = xor(vector, shift(shift(shift(char4))))
    return vector

def create_5_gram(char1, char2, char3, char4, char5):
    vector = xor(char1, shift(char2))
    vector = xor(vector, shift(shift(char3)))
    vector = xor(vector, shift(shift(shift(char4))))
    vector = xor(vector, shift(shift(shift(shift(char5)))))
    return vector

def create_3_gram(char1, char2, char3):
    vector = xor(char1, shift(char2))
    vector = xor(vector, shift(shift(char3)))
    return vector

#fehlerhaft
def bundle(matrix):
    np_matrix = np.array(matrix)
    num_of_rows = np_matrix.shape[0]
    np_vector = np.sum(np_matrix, axis = 0)
    np_result_vector = np.where(np_vector/num_of_rows >= 0.5,1,0) 
    return np_result_vector

def return_char_array(line):
    line = line.strip()
    char_array= []
    for char in line:
        char_array.append(char)
    np_char_array = np.array(char_array)
    return np_char_array

#def create_char_hypervectors_file():
#    with open(char_hypervectors_file, 'w') as file:
#        for char, hypervector in char_hypervectors.items():
#            #file.write(f"{char}: {hypervector}\n")
#            hypervector_str = ' '.join(map(str, hypervector))
#            file.write(f"{char}: {hypervector_str}\n")

def write_dict_to_file(path, vector):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as file:
        for identifier, data in vector.items():
            try:
                data_str = ' '.join(map(str, data))
            except Exception as e:
             # Skip the operation if there's an error
                data_str = data  # or use `pass` if you want to do nothing
            #data_str = ' '.join(map(str, data))
            file.write(f"{identifier}: {data_str}\n")    

def append_data_to_file(path, identifier, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'a') as file:
        data_str = ' '.join(map(str, data))
        file.write(f"{identifier}: {data_str}\n")

def remove_file(path):
    if os.path.exists(path):
        os.remove(path)
        print(f"file {path} removed")
    else:
        print('no file had to be removed')
        pass

def import_dict_from_txt(file_path):
    with open(file_path, 'r') as file:
        print(file_path)
        key_array = []
        value_array = []
        for line in file:
            key, value = line.split(':',1)
            #key_array.append(key.strip())
            key_array.append(key)
            value = value.strip().split()
            value_array.append([int(bit) for bit in value])
            #value_array.append([int(bit) for bit in value.strip()])
        dict_from_file = dict(zip(key_array, value_array))               
    return dict_from_file

def import_values_from_txt(file_path):
    with open(file_path, 'r') as file:
        print(file_path)
        value_array = []
        for line in file:
            key, value = line.split(':',1)
            #key_array.append(key.strip())
            value = value.strip().split()
            value_array.append([int(bit) for bit in value])
    return value_array 


def return_file(iterator, paths):
    file = open(paths[iterator], 'r')
    return file

def has_more_than_n_files(directory_path, n):
    entries = os.listdir(directory_path)
    files = [entry for entry in entries if os.path.isfile(os.path.join(directory_path, entry))]
    # Check if the number of files is exactly n
    return len(files) >= n

def choose_dimension(context):
    training_context = 2
    testing_context = 12
    result_context = 13
    if context == 'training':
        n_files = training_context
    elif context == 'testing':
        n_files = testing_context
    elif context == 'result':
        n_files = result_context
        
    for value in dimensions:
        directory_name = f'dimension_{value}'
        directory_path = os.path.join(base_directory, directory_name)
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            if has_more_than_n_files(directory_path, n_files):
                print(f"Directory {directory_name} exists. Moving to next one ...")
            else:
                print(f"Directory {directory_name} doesN't exist. Further files need to be created. Proceeding from here ...")
                return value
        else:
            print(f"Directory {directory_name} does not exist. Proceeding from here ...")
            return value
    print('all dimensions were trained, exiting ...')
    sys.exit()    


def get_test_sets(dimension, language_training_file, char_training_file, trained_char_hypervectors, paths, identifiers, lang_iterator):
    #setup, returning file and empty matrix and iterator
    file = return_file(lang_iterator, paths) #returns the /dataset/testing file for the language
    document_matrix  = []
    iterator = 0 #line iterator definition
    file_path = f'{base_directory}/dimension_{dimension}/{identifiers[lang_iterator]}.txt' #created dataset savepoint -> this file will have the structure of a python dict
    remove_file(file_path)
    identifier = identifiers[lang_iterator]
    
    #iterating over the lines and putting each line into a vector and bundling this in a matrix
    for line in tqdm(file):
        iterator = iterator + 1
        np_char_array = return_char_array(line)   
        line_matrix = []
        
        for i in range(len(np_char_array) - 3):
            np_char_array1 = return_nparray(np_char_array[i], trained_char_hypervectors)
            np_char_array2 = return_nparray(np_char_array[i+1], trained_char_hypervectors)
            np_char_array3 = return_nparray(np_char_array[i+2], trained_char_hypervectors)
            np_char_array4 = return_nparray(np_char_array[i+3], trained_char_hypervectors)
            
            
            charvector = create_4_gram(np_char_array1,  np_char_array2,  np_char_array3,  np_char_array4)
            line_matrix.append(charvector)
        document_matrix.append(bundle(line_matrix))
                    
        #after 50 loops, 50 lines are added to the output file
        if iterator == 50: #once the matrix grew to 50 all the data will be appended to the file
            while iterator > 0:
                append_data_to_file(file_path, identifier, document_matrix[iterator-1])
                iterator = iterator - 1
            iterator = 0
            document_matrix = []
            print(f"writing into {file_path} ...")
    
    #adding the last lines to the file if the above for loop is finished
    iterator = len(document_matrix)
    while iterator > 0:
        append_data_to_file(file_path, identifier, document_matrix[iterator-1])
        iterator = iterator - 1
    pass    


def accuracy_calc(dimension, language_training_file_hypervectors, language_training_file_hypervectors_values, language_training_file_hypervectors_identifiers ,my_dict, iterator):
    language_testing_file = f'{base_directory}/dimension_{dimension}/{language_training_file_hypervectors_identifiers[iterator]}.txt'
    language_testing_file_hypervectors_values = import_values_from_txt(language_testing_file)

    correct_language = language_training_file_hypervectors_identifiers[iterator]
    correct_language_cnt = 0
    
    for line in language_testing_file_hypervectors_values:
        Min_distance = float('inf')
        for key, value in language_training_file_hypervectors.items():
            distance = hamming_distance(line, value)
            if distance < Min_distance:
                Min_distance = distance
                closest_language = key

        if closest_language == correct_language:
            correct_language_cnt += 1

    my_dict[correct_language] = correct_language_cnt/1000
    return(1)



def hamming_distance(vec1, vec2):
    return distance.hamming(vec1, vec2) * len(vec1)


def train_set():
    dimension = choose_dimension('training')
    print(f"training set with {dimension} dimensions\n")
    
    char_hypervectors = {char: np.random.randint(0, 2, dimension) for char in characters}
    language_training_file = f'{base_directory}/dimension_{dimension}/training_language.txt'
    char_training_file = f'{base_directory}/dimension_{dimension}/training_characters.txt'
    remove_file(language_training_file)
    remove_file(char_training_file)
    paths = list(bic_training_file_array.values())
    identifiers = list(bic_training_file_array.keys())
    file_iterator = len(bic_training_file_array) - 1
    while file_iterator >= 0:
        file = return_file(file_iterator, paths)
        document_matrix  = []
        for line in tqdm(file):
            np_char_array = return_char_array(line)   
            line_matrix = []

            for i in range(len(np_char_array) - 3):
                np_char_array1 = return_nparray(np_char_array[i], char_hypervectors)
                np_char_array2 = return_nparray(np_char_array[i+1], char_hypervectors)
                np_char_array3 = return_nparray(np_char_array[i+2], char_hypervectors)
                np_char_array4 = return_nparray(np_char_array[i+3], char_hypervectors)
                charvector = create_4_gram(np_char_array1,  np_char_array2,  np_char_array3,  np_char_array4)
                line_matrix.append(charvector)

            document_matrix.append(bundle(line_matrix))

        #print(document_matrix)
        document_vector = bundle(document_matrix)
        print(...)
        append_data_to_file(language_training_file, identifiers[file_iterator], document_vector)
        file_iterator = file_iterator - 1

    write_dict_to_file(char_training_file, char_hypervectors)
    #create_char_hypervectors_file()
    train_set()

def test_set():
    dimension = choose_dimension('testing')
    print(f"testing set with {dimension} dimensions\n")

    language_training_file = f'{base_directory}/dimension_{dimension}/training_language.txt'
    char_training_file = f'{base_directory}/dimension_{dimension}/training_characters.txt'
    trained_char_hypervectors = import_dict_from_txt(char_training_file)
    paths = list(bic_testing_file_array.values())
    identifiers = list(bic_testing_file_array.keys())
    

    #start multiprocessing
    processes = []
    for lang_iterator in range(len(bic_testing_file_array)):
        process = multiprocessing.Process(target=get_test_sets, args=(dimension, language_training_file, char_training_file, trained_char_hypervectors, paths, identifiers, lang_iterator-1) )
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
    
    test_set()

def result():
    dimension = choose_dimension('result')
    print(f"extracting results for dimension {dimension}\n")
    language_training_file = f'{base_directory}/dimension_{dimension}/training_language.txt'
    language_training_file_hypervectors = import_dict_from_txt(language_training_file)
    language_training_file_hypervectors_identifiers = list(language_training_file_hypervectors.keys())
    language_training_file_hypervectors_values = list(language_training_file_hypervectors.values())
    result_file = f'{base_directory}/dimension_{dimension}/results.txt'
    my_dict = multiprocessing.Manager().dict()

    #start multiprocessing
    processes = []
    for lang_iterator in range(len(language_training_file_hypervectors_identifiers)):
    #for lang_iterator in range(1):
        process = multiprocessing.Process(target=accuracy_calc, args=(dimension, language_training_file_hypervectors, language_training_file_hypervectors_values, language_training_file_hypervectors_identifiers, my_dict, lang_iterator-1))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
    
    
    print(my_dict)
    write_dict_to_file(result_file, my_dict)
    result()

    

def default_case():
    print("Invalid selection")

def switch_case(user_input):
    if user_input == '1':
        return train_set()
    elif user_input == '2':
        return test_set()
    elif user_input == '3':
        #cosine similarity
        return result()
    else: 
        return default_case()


def main():

    user_input = input("Enter a case (1: training, or 2: testing, or 3: accuracy results): ")
    result = switch_case(user_input)    



if __name__ == "__main__":
    main()
    print("finished")