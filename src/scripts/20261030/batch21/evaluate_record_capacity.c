#include "scr_record_capacity.h"
float evaluate_record_capacity(void)
{
    requested_capacity_mode = dispatch_argument0;
    capacity_result = 0;
    if (requested_capacity_mode == 0) {
        sampled_unoccupied_count = get_unoccupied_native_record_count();
        if (1 <= sampled_unoccupied_count) {
            capacity_result = 1;
        }
    } else {
        if (requested_capacity_mode == 1) {
            sampled_unoccupied_count = get_unoccupied_native_record_count();
            if (2 <= sampled_unoccupied_count) {
                capacity_result = 1;
            }
        } else {
            if (requested_capacity_mode == 2) {
                sampled_unoccupied_count = get_unoccupied_native_record_count();
                if (3 <= sampled_unoccupied_count) {
                    capacity_result = 1;
                }
            }
        }
    }
    return capacity_result;
}
