#include <lambdas.h>

// Simulation is not trimmed, zeros at the tail must be eliminated
void compute_lambdas(double * simulation, double * lambda_result,
                     double * mus, double * alphas, double * betas,
                     int dim,
                     int target_index,
                     int * current_indices,
                     int n_points){
    if(current_indices[target_index] < 2) return;
    double * past_values = (double *) malloc(dim * sizeof(double));
    double * present_values = (double *) malloc(dim * sizeof(double));
    int * start_indices = (int *) malloc(dim * sizeof(int));
    int * stop_indices = (int *) malloc(dim * sizeof(int));
    double t_start = 0.0;
    double t_stop = 0.0;
    double old_t_start = 0.0;
    double old_t_stop = 0.0;
    int found_start;
    double s_p;
    double current_beta;
    double current_alpha;
    // Initializing start and stop indices
    for(int p = 0; p < dim; ++p){
        past_values[p] = 0.0;
        present_values[p] = 0.0;
        start_indices[p] = 0;
        stop_indices[p] = 1;
    }
    // Looping over points of target_index
    for(int i = 0; i < current_indices[target_index] - 1; ++i){
        t_start = simulation[target_index*n_points + i];
        t_stop = simulation[target_index*n_points + i + 1];
        if((t_start == 0.0) || (t_stop == 0)){
            break;
        }
        lambda_result[i] = (t_stop - t_start) * mus[target_index];
        //Getting the values of the intermediate terms
        for(int p = 0; p < dim; ++p){
            current_alpha = alphas[target_index*dim + p];
            current_beta = betas[target_index*dim + p];
            if(current_beta == 0){
                continue;
            }
            //Updating past_values
            if(i > 0){
                past_values[p] *=
                    (exp(-current_beta * t_start) - exp(-current_beta * t_stop)) /
                        (exp(-current_beta * old_t_start) - exp(-current_beta * old_t_stop));
                for(int j = start_indices[p]; j < stop_indices[p]; ++j){
                    s_p = simulation[p*n_points + j];
                    past_values[p] += exp(-current_beta * (t_start - s_p))
                        - exp(-current_beta * (t_stop - s_p));
                }
            }
            //Getting start and stop indices
            found_start = 0;
            for(int j = 0; j < current_indices[p]; ++j){
                s_p = simulation[p*n_points + j];
                if(s_p == 0){
                    continue;
                }
                if((!found_start)
                   &&(s_p >= t_start)
                   &&(s_p < t_stop)){
                    found_start = 1;
                    start_indices[p] = j;
                }else{
                    if(s_p > t_stop){
                        if(j == 0){
                            stop_indices[p] = j;
                        }else{
                            stop_indices[p] = j - 1;
                        }
                        break;
                    }
                }
            }
            //Setting up past_values for the first time
            if(i == 0){
                for(int j = 0; j < start_indices[p]; ++j){
                    s_p = simulation[p*n_points + j];
                    past_values[p] += exp(-current_beta * (t_start - s_p))
                        - exp(-current_beta * (t_stop - s_p));
                }
            }
            //Updating present values
            present_values[p] = 0.0;
            for(int j = start_indices[p]; j < stop_indices[p]; ++j){
                s_p = simulation[p*n_points + j];
                present_values[p] += 1.0 - exp(-current_beta * (t_stop - s_p));
            }
            //Updating lambda
            lambda_result[i] += (current_alpha / current_beta) * (past_values[p] + present_values[p]);
        }
        old_t_start = t_start;
        old_t_stop = t_stop;
    }
    free(past_values);
    free(present_values);
    free(start_indices);
    free(stop_indices);
}