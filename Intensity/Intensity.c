#include <Intensity.h>

// Simulation is not trimmed, zeros at the tail must be eliminated
void compute_intensities(double * simulation,
                          double * targets,
                          double * results,
                          double * mus, double * alphas, double * betas,
                          int dim,
                          int target_index,
                          int * current_indices,
                          int n_points,
                          int n_targets){
    if(current_indices[target_index] < 2) return;
    double * temp_values = (double*) malloc(dim * sizeof(double));
    double s_p;
    double current_alpha;
    double current_beta;
    double current_mu;
    double last_second = simulation[target_index*n_points + current_indices[target_index] - 1];
    // Setting up stop indices
    int * stop_indices = (int*) malloc(dim * sizeof(int));
    for(int p = 0; p < dim; ++p){
        stop_indices[p] = 0;
        temp_values[p] = 0.0;
    }
    // Computing intensities
    double t_i;
    double old_t_i = 0.0;
    double intensity;
    for(int i = 0; i < n_targets; ++i){
        t_i = targets[i];
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
                // Make sure the last point is used once and once only
                if(j == current_indices[p] - 1){
                    stop_indices[p] = current_indices[p];
                }
            }
            intensity += temp_values[p];
        }
        results[i] = intensity;
        old_t_i = t_i;
    }
    free(temp_values);
    free(stop_indices);
}