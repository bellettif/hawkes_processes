#ifndef HP_SIMULATOR_H
#define HP_SIMULATOR_H

#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "mt19937.h"

// This class implements a simulator of Self-exciting point processes
// with exponentially decaying kernels

// Initialize the random generator mt19937 with the seed s
void init_exp_genrand(unsigned long s);

// Function that is used in order to simulate the time until next jump
double get_next_exp(double lambda);

// Simulate a new trajectory
/*
 * n_second is the total period of simulation
 *
 * dim is the number of dimensions of the process
 *
 * mus, alphas and betas are the parameters of the simulation.
 * The 2-dimensional matrices are transformed in one-dimensional arrays.
 * So to access the ith parameter of the jth component of alphas and betas,
 * the index is i + j * dim.
 *
 * current_indices will return the last indices of the jumps
 * for each process. The array containing the resulting jumps is
 * not trimmed at the end of the simulation so we need to keep
 * the last indices in memory
 *
 * max_points is the maximum number of jumps that will be simulated
 * for a given component. The total length of the one-dimensional array
 * containing the jumps will be dim * max_points
 *
 * result is a one-dimensional array that contains the jumps, the strides
 * are max_points long. So to access the ith jumps of the jth component, the index
 * is i + j * max_points.
 *
 */
void next_simulation(double n_seconds,
                     int dim,
                     double * mus,
                     double * alphas,
                     double * betas,
                     int * current_indices,
                     int max_points, double * result);

// Thinning method (acceptance/rejection + selects the component
// that will be given the next jump if any)
double attribution(double * values, double cur_max, int dim);

// Used in order to compute the current intensity of a component
double sum_of_row(double * alphas, int target_row, int dim);

#endif
