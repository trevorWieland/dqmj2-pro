#include "scr_formal_decision.h"
void enable_primary_24_from_argument(float request)
{
    if (request == 5) {
        float state = get_numeric_state(0);
        if (state == 2) {
            state = get_numeric_state(3);
            if (state == 6) {
                set_primary_flag(24, true);
            }
        }
    }
}
