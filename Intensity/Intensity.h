#ifndef INTENSITY_H
#define INTENSITY_H

#include<math.h>
#include<stdlib.h>

// C code that computes the intensity of a generated self-exciting
// process trajectory
/*
 * Simulation is the array of simulated jumps (1 dimensional array)
 * In order to access the ith jump of the jth component, the index
 * is n_points * j + i.
 *
 * Targets is the instants at which the intensity will be computed.
 *
 * Result will contain the computed intensities.
 *
 * Mus, alphas and betas are the simulation parameters. In order to access
 * the ith parameter of the jth component of alphas and betas, the index is dim * j + i.
 *
 * Dim is the number of components of the simulated trajectory.
 *
 * Target_index is the index of the component for which intensity should
 * be computed.
 *
 * Current_indices are the trimming indices of the simulation.
 *
 * N_points is the stride of the simulation array.
 *
 * N_targets is the number of instants for which intensity will be computed.
 */
void compute_intensities(double * simulation,
                           double * targets,
                           double * result,
                           double * mus, double * alphas, double * betas,
                           int dim,
                           int target_index,
                           int * current_indices,
                           int n_points,
                           int n_targets);

#endif
