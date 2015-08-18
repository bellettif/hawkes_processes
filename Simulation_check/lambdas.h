#ifndef LAMBDAS_H
#define LAMBDAS_H

#include<math.h>
#include<stdlib.h>

/*
 * This function computes the normalized times of a self-exciting point process
 *
 * simulation is the array of simulated trajectories (each array comtains
 * the jumps of a given component)
 *
 * lambda_result will contain the computed normalized times between consecutive
 * jumps
 *
 * mus, alphas and betas are the normalization parameters, they should
 * be the same as the simulation parameters
 *
 * dim is the number of components in the process
 *
 * target_index is the index of the component for which the normalized times will be
 * computed
 *
 * current_indices contains the index of the last jump for each component
 *
 * n_points is the number of jumps for the given component
 *
 */
void compute_lambdas(double * simulation, double * lambda_result,
                     double * mus, double * alphas, double * betas,
                     int dim,
                     int target_index,
                     int * current_indices,
                     int n_points);

#endif
