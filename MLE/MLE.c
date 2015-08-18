#include <MLE.h>

// Simulation is not trimmed, zeros at the tail must be eliminated
double compute_likelihood(double * simulation,
                        double * mus, double * alphas, double * betas,
                        int dim,
                        int target_index,
                        int * current_indices,
                        int n_points){
    if(current_indices[target_index] < 2) return 0.0;
    double * temp_values = (double*) malloc(dim * sizeof(double));
    double s_p;
    double current_alpha;
    double current_beta;
    double current_mu;
    double last_second = simulation[target_index*n_points + current_indices[target_index] - 1];
    double result = (1.0 - mus[target_index]) * last_second;
    // Setting up stop indices
    int * stop_indices = (int*) malloc(dim * sizeof(int));
    for(int p = 0; p < dim; ++p){
        stop_indices[p] = 0;
    }
    // Computing last uppercase lambda
    for(int p = 0; p < dim; ++p){
        temp_values[p] = 0;
        current_alpha = alphas[dim*target_index + p];
        current_beta = betas[dim*target_index + p];
        if(current_beta == 0.0) continue;
        for(int j = 0; j < current_indices[p]; ++j){
            s_p = simulation[p*n_points + j];
            if(s_p == 0.0) break;
            if(s_p > last_second) break;
            temp_values[p] += 1.0 - exp(-current_beta*(last_second - s_p));
        }
        temp_values[p] *= current_alpha / current_beta;
        result -= temp_values[p];
    }
    // Resetting temp_values
    for(int p = 0; p < dim; ++p){
        temp_values[p] = 0.0;
    }
    // Computing lower case lambdas
    double t_i;
    double old_t_i = 0.0;
    double intensity;
    for(int i = 0; i < current_indices[target_index]; ++i){
        t_i = simulation[target_index*n_points + i];
        if(t_i == 0.0) break;
        intensity = mus[target_index];
        for(int p = 0; p < dim; ++p){
            current_alpha = alphas[dim*target_index + p];
            current_beta = betas[dim*target_index + p];
            if(current_beta == 0.0) continue;
            if(current_alpha == 0.0) continue;
            // Updating temp_values with exponential decay
            temp_values[p] *= exp(- current_beta * (t_i - old_t_i));
            for(int j = stop_indices[p]; j < current_indices[p]; ++j){
                s_p = simulation[p*n_points + j];
                if(s_p == 0.0) break;
                if(s_p > t_i){
                    stop_indices[p] = j;
                    break;
                }
                temp_values[p] += current_alpha * exp(- current_beta * (t_i - s_p));
            }
            intensity += temp_values[p];
        }
        result += log(intensity);
        old_t_i = t_i;
    }
    free(temp_values);
    free(stop_indices);
    return result;
}