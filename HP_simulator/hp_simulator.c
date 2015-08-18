#include "hp_simulator.h"

void init_exp_genrand(unsigned long s){
    init_genrand(s);
}

double get_next_exp(double lambda){
    return - log(genrand_real3()) / lambda;
}

//
// Current indices must be initialized at -1, it will indicate the last index
// of the jumps millisecond positions
// -1 means here that there was no jump for the given dimension
//
// If result == 0 it means there was not jump at all
//
void next_simulation(double n_seconds,
                     int dim, double * mus,
                     double * alphas, double * betas,
                     int * current_indices,
                     int max_points, double * result){
	double max_int = 0;
	double current_s = 0;
    // Memory initialization
	for(int i = 0; i < dim; ++i){
		max_int += mus[i];
        current_indices[i] = 0;
	}
	current_s += get_next_exp(max_int);
	if(current_s > n_seconds){
		return;
	}
	int attributed = dim;
	double ** last_contingent_int = (double **) malloc(dim * sizeof(double *));
    // last contingent int is last intensity computation, only valid for exp kernel
	for(int i = 0; i < dim ; ++i){
		last_contingent_int[i] = (double*) malloc(dim * sizeof(double));
		for(int j=0 ; j < dim; ++ j){
			last_contingent_int[i][j] = 0;
		}
	}
	// Attribution
	attributed = attribution(mus, max_int, dim);
    if(attributed == dim){
        attributed = dim - 1;
    }
	// Update first chosen millisecond
	result[attributed*max_points + current_indices[attributed]] = current_s;
    current_indices[attributed] ++;
	// Update last_contingent_intensities
	for(int i = 0 ; i < dim; ++i){
		last_contingent_int[i][attributed] = alphas[i*dim + attributed];
	}
	// Update max intensity
	max_int += sum_of_row(alphas, attributed, dim);
	// General algorithm
	double * current_ints = (double *) malloc(dim * sizeof(double));
    for(int i = 0; i < dim; ++i){
        current_ints[i] = mus[i];
        for(int j = 0; j < dim ; ++j){
            if(current_indices[j] > 0){
                current_ints[i] += last_contingent_int[i][j];
            }
        }
    }
	unsigned long delta_t = 0;
	unsigned long last_calc_point = 0;
	while(current_s < n_seconds){
		last_calc_point = current_s;
		// Get the next candidate
		current_s += get_next_exp(max_int);
		attributed = attribution(current_ints, max_int, dim);
		if(attributed == dim){
            max_int = 0.0;
			// Attribution failed, decrease max intensity
            for(int i = 0; i < dim; ++i){
                current_ints[i] = mus[i];
                for(int j = 0; j < dim ; ++j){
                    if(current_indices[j] > 0){
                        delta_t = current_s - last_calc_point ;
                        last_contingent_int[i][j] *= exp( - (betas[i*dim + j] * delta_t));
                        current_ints[i] += last_contingent_int[i][j];
                        max_int += current_ints[i];
                    }
                }
            }
		}else{
			// Attribution succeeded, increase max intensity
            if(current_indices[attributed] == max_points){
                printf("%s\n","MAXIMUM NUMBER OF POINTS REACHED, INVALID SIMULATION");
                current_s = n_seconds + 1; // Force exit the while loop
            }else
            {
				for(int i = 0; i < dim; ++i){
					max_int += alphas[i*dim + attributed];
					for(int j = 0; j < dim ; ++j){
						if(current_indices[j] > 0){
							delta_t = current_s - last_calc_point ;
							last_contingent_int[i][j] *= exp( - (betas[i*dim + j] * delta_t));
						}
					}
					last_contingent_int[i][attributed] += alphas[i*dim + attributed];
				}
				result[attributed*max_points + current_indices[attributed]] = current_s;
				current_indices[attributed] ++;
            }
		}
	}
    // Deleting last contingent intensities
    for(int i = 0; i < dim; ++i){
        free(last_contingent_int[i]);
    }
    free(last_contingent_int);
    free(current_ints);
}

//
// Attribution of the next jump.
// Returns the index for which there will be a jump.
// If no allocation, returns dim
//
double attribution(double* values, double cur_max, int dim){
	double choice = genrand_real3();
	double sum = 0;
	double next = 0;
	for(int i = 0; i < dim; ++i){
		next = sum + (values[i] / cur_max);
		if((choice >= sum) && (choice < next)){
			return i;
		}else{
			sum = next;
		}
	}
	return dim;
}

double sum_of_row(double * alphas, int target_row, int dim){
	double sum = 0;
	for(int j = 0; j < dim; ++j){
		sum += alphas[target_row*dim + j];
	}
	return sum;
}
