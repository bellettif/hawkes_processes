#include "add_traj.h"

void add_traj(double * minus_traj, double * plus_traj,
              double * result_ts, double * result_values,
              int minus_length, int plus_length){
    int i_minus = 0;
    int i_plus = 0;
    int i = 0;
    int current_value = 0;
    while((i_minus < minus_length)||(i_plus < plus_length)){
        if(i_minus == minus_length){
            result_ts[i] = plus_traj[i_plus];
            current_value += 1.0;
            result_values[i] = current_value;
            i ++;
            i_plus++;
            continue;
        }
        if(i_plus == plus_length){
            result_ts[i] = minus_traj[i_minus];
            current_value -= 1.0;
            result_values[i] = current_value;
            i ++;
            i_minus ++;
            continue;
        }
        if((minus_traj[i_minus]) <= (plus_traj[i_plus])){
            result_ts[i] = minus_traj[i_minus];
            current_value -= 1.0;
            i_minus ++;
        }else{
            result_ts[i] = plus_traj[i_plus];
            current_value += 1.0;
            i_plus ++;
        }
        result_values[i] = current_value;
        i ++;
    }
}