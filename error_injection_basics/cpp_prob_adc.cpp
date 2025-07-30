#include <stdio.h>
#include <time.h>
#include <vector>
#include <numeric>
#include <algorithm>
#include <string>
#include <tuple>
#include <iostream>
#include <fstream>
#include <random>
#include <limits>
#include <boost/dynamic_bitset.hpp>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

using namespace std;

typedef boost::dynamic_bitset<> bits;
typedef vector<bits> block_vector;
typedef vector<tuple<string, block_vector>> block_vector_set;


inline int probabilistic_adc(int ham_dist, vector<discrete_distribution<>> &adc_model, mt19937 &gen){
    // call by reference is essential for gen as only then it steps forward
    return adc_model[ham_dist](gen);
}

double do_inference(const block_vector_set &block_class_vectors, const block_vector_set &block_test_vectors, vector<discrete_distribution<>> &adc_model, mt19937 &gen){
    int best_hd, cur_hd, software_hd, hardware_hd;
    string best_class_label;
    int correct_results = 0;

    // To get a "hardware Hamming distance" from the model:
    // hardware_hd = probabilistic_adc(software_hd, adc_model, gen);

    for (auto [test_label, test_vec] : block_test_vectors){
        // Do inference of test vector using the hardware model on each block
        // ...
        
    }
    return ((double) correct_results) / block_test_vectors.size();
}

// We use only full blocks, i.e., the cut away at the end will be discarted
block_vector* make_block_vector_floor(string bit_vector, int block_size){
    block_vector *res_vec = new block_vector;
    int dim = bit_vector.length();
    int num_of_blocks = dim / block_size;
    int length;
    int start;
    for (int n = 0; n < num_of_blocks; n++){
        start = n * block_size;
        bits bit_block(bit_vector.substr(start, block_size));
        res_vec->push_back(bit_block);
    }
    return res_vec;
}

/*
* The input adc model matrix needs to be of the following form:
* Square matrix including the row and column for the 0 Hamming distance (HD)
* The precision can not be greater than the largest simulated HD (e.g. block size of 15, but you simulated only until a HD of 10 to save time)
* The matrix needs to be in row-major orientation and each row describes the probability distribution of this HDs, row 0 corrisponds to HD 0
*/
vector<discrete_distribution<>>* prepare_adc_model(const vector<vector<double>> &adc_model_matrix, int precision, int block_size){
    vector<discrete_distribution<>> *distribution_matrix = new vector<discrete_distribution<>>;

    assert(adc_model_matrix.size() == adc_model_matrix[0].size());
    int prec_idx = precision + 1;
    assert(prec_idx <= adc_model_matrix.size());

    if (precision < block_size) {
        for (auto row : adc_model_matrix){
            vector<double> pruned = vector<double>(row.begin(), row.begin()+prec_idx);
            pruned[pruned.size()-1] += accumulate(row.begin()+prec_idx, row.end(), 0.0);
            distribution_matrix->push_back(discrete_distribution<>(pruned.begin(), pruned.end()));
            assert(abs(1.0-accumulate(pruned.begin(), pruned.end(), 0.0)) < 1e-5);
        }
        vector<double> filler_row(prec_idx, 0.0);
        filler_row[filler_row.size()-1] = 1.0;
        for (int i = 0; i < block_size + 1 - adc_model_matrix.size(); ++i){
            distribution_matrix->push_back(discrete_distribution<>(filler_row.begin(), filler_row.end()));
        }
    } else {
        for (auto out_distribution : adc_model_matrix){
            distribution_matrix->push_back(discrete_distribution<>(out_distribution.begin(), out_distribution.end()));
        }
    }
    assert(distribution_matrix->size() == block_size+1);

    return distribution_matrix;
}


size_t sysrandom(void* dst, size_t dstlen){
    char* buffer = reinterpret_cast<char*>(dst);
    std::ifstream stream("/dev/urandom", std::ios_base::binary | std::ios_base::in);
    stream.read(buffer, dstlen);
    return dstlen;
}

/*
* To call this function from python, import the compiled shared library (the .so file) in your python script, e.g.:
* import cpp_prob_adc
* cpp_prob_adc.inference_with_errors(<parameters>)
* 
* pybind11 will take care of the type casts for python types to C++ types.
* Eg. a python list of tuples will be casted to a C++ vector of tuples.
*/
vector<double> inference_with_errors(vector<tuple<string, string>> class_vectors, vector<tuple<string, string>> test_vectors, int num_of_samples, int block_size, int precision, vector<vector<double>> adc_model_matrix){
    block_vector_set block_class_vectors;
    for (auto [class_label, vector_string] : class_vectors){
        block_class_vectors.push_back(make_tuple(class_label, *make_block_vector_floor(vector_string, block_size)));
    }

    block_vector_set block_test_vectors;
    for (auto [querry_label, vector_string] : test_vectors){
        block_test_vectors.push_back(make_tuple(querry_label, *make_block_vector_floor(vector_string, block_size)));
    }

    std::uint_least32_t seed;    
    sysrandom(&seed, sizeof(seed));
    std::mt19937 gen(seed);

    vector<discrete_distribution<>> distribution_matrix = *prepare_adc_model(adc_model_matrix, precision, block_size);


    vector<double> result_accuracies(num_of_samples, 0.0);
    for (int i = 0; i < num_of_samples; i++){
        result_accuracies[i] = do_inference(block_class_vectors, block_test_vectors, distribution_matrix, gen);
    }

    //no free is needed as it automatically frees the memory by returning to python

    return result_accuracies;
}

// the following functions might be helpful for debugging 
void print_vector(vector<double> vec){
    for (auto elem : vec){
        cout << elem << ", ";
    }
    cout << endl;
}

void print_block_vec(block_vector vec){
    string buffer;
    for (bits block : vec){
        boost::to_string(block, buffer);
        cout << buffer << " ";
    }
    cout << endl;
}

void print_vec_set(block_vector_set data){
    for (auto [label, vec] : data){
        cout << label << " | ";
        print_block_vec(vec);
    }
    cout << endl;
}

void print_adc_model(vector<discrete_distribution<>> *adc_model) {
    for (auto i : *adc_model){
        cout << i << endl;
    }
}




PYBIND11_MODULE(cpp_prob_adc, m) {
    m.doc() = "C++ implementation of the probabilistic adc that computes inference accuracies for multiple samples based on given discrete distribution";

    m.def("inference_with_errors", &inference_with_errors, "Compute a list of inference accuracies based on given class, test vectors and provided discrete distribution for the prob. ADC.");
}