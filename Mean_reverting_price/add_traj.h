#ifndef ADD_TRAJ_H
#define ADD_TRAJ_H

#include<stdlib.h>

// Here we make the asumption that minus and plus have no common jumps
// which is always the case with our simulation algorithm.
// This is used to compute a mean-reverting stock price.
/*
 *  Minus traj contains the negative price jumps
 *  Plus traj contains the positive price jumps
 *  Result_ts contains the timestamps of the result
 *  Result_values contains the prices corresponding to the timestamps
 *
 */
void add_traj(double * minus_traj, double * plus_traj,
              double * result_ts, double * result_values,
              int minus_length, int plus_length);

#endif
