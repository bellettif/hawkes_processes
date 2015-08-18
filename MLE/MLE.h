#ifndef MLE_H
#define MLE_H

#include<math.h>
#include<stdlib.h>

// Compute the log likelihood of a component for a given simulated
// trajectory and a given set of mu, alpha and beta parameters
/*
 * Simulation is the multi-dimensional simulated Self-exciting
 * Point Process. In order to access the ith jump of
 * the jth component, the index is j * n_points + i.
 *
 * Mus, alphas and betas are the candidates for the likelihood ratio.
 * For alphas and betas, in order to access the ith parameter of the
 * jth component, the index is j * dim + i.
 *
 * dim is the number of components.
 *
 * target_index is the index of components which likelihood will be
 * computed.
 *
 * Current_indices are the trimming indices for the simulation.
 *
 * n_points is the horizontal dimension of simulatioN.
 */
double compute_likelihood(double * simulation,
                          double * mus, double * alphas, double * betas,
                          int dim,
                          int target_index,
                          int * current_indices,
                          int n_points);

#endif
