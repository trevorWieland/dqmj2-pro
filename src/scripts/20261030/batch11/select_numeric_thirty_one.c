#include "scr_random_decision.h"
void select_numeric_thirty_one(void)
{
    bool enabled = get_primary_flag(93);
    if (enabled == false) {
        return;
    }
    enabled = get_primary_flag(28);
    if (enabled == true) {
        return;
    }
    float state = get_numeric_state(32);
    if (state < 4) {
        set_numeric_state(32, 4);
    } else {
        if (8 <= state) {
            return;
        }
    }
    float selection = sample_signed_random(6);
    if (selection == 0) {
        set_numeric_state(31, 6);
    } else {
        if (selection == 1) {
            set_numeric_state(31, 19);
        } else {
            if (selection == 2) {
                set_numeric_state(31, 31);
            } else {
                if (selection == 3) {
                    set_numeric_state(31, 43);
                } else {
                    if (selection == 4) {
                        set_numeric_state(31, 49);
                    } else {
                        if (selection == 5) {
                            set_numeric_state(31, 59);
                        }
                    }
                }
            }
        }
    }
}
