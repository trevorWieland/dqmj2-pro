#include "scr_formal_decision.h"
void clear_primary_24_from_argument(float request)
{
    float state;
    if (request == 8) {
        state = get_numeric_state(0);
        if (state == 2) {
            state = get_numeric_state(3);
            if (state == 6) {
                set_primary_flag(24, false);
            }
        }
    } else {
        if (request == 15) {
            state = get_numeric_state(0);
            if (state == 2) {
                state = get_numeric_state(3);
                if (state == 8) {
                    set_primary_flag(24, false);
                }
            }
        }
    }
}
