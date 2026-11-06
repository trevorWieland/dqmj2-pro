#include "scr_reset_caller.h"
void reset_world_flags(float saved_input)
{
    set_primary_flag(2, false);
    set_primary_flag(62, false);
    set_primary_flag(61, false);
    reset_runtime_counter(0);
    set_primary_flag(289, false);
    set_primary_flag(318, false);
    set_primary_flag(320, false);
    set_primary_flag(322, false);
    set_primary_flag(324, false);
    set_primary_flag(328, false);
    set_primary_flag(319, false);
    set_primary_flag(331, false);
    set_primary_flag(332, false);
    set_primary_flag(330, false);
    set_primary_flag(325, false);
    set_primary_flag(321, false);
    set_primary_flag(323, false);
    set_primary_flag(329, false);
    set_primary_flag(333, false);
    set_primary_flag(363, false);
    set_primary_flag(338, false);
    set_primary_flag(351, false);
    set_primary_flag(352, false);
    for (int flag = 346; flag < 350; ++flag) {
        set_primary_flag(flag, false);
    }
    for (int flag = 500; flag < 510; ++flag) {
        set_primary_flag(flag, false);
    }
    for (int flag = 245; flag < 252; ++flag) {
        set_primary_flag(flag, false);
    }
    set_primary_flag(259, false);
    for (int flag = 252; flag < 259; ++flag) {
        set_primary_flag(flag, false);
    }
    for (int flag = 273; flag < 281; ++flag) {
        set_primary_flag(flag, false);
    }
    set_primary_flag(271, false);
    float sampled_value = sample_signed_random(7);
    set_numeric_state(52, sampled_value);
    bool runtime_limit = runtime_counter_at_threshold();
    set_primary_flag(145, runtime_limit);
    reset_shared_flags();
    advance_world_numeric_state();
    refresh_shared_context();
    run_world_context_updates();
    apply_saved_world_argument(saved_input);
    before_primary_flag_reset();
    finalize_world_state();
}
