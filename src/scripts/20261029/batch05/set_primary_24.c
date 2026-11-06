#include "scr_numeric.h"
void set_primary_24_when_numeric_values_match(void)
{
    float context_value = get_context_value(0);
    float state_zero = get_numeric_state(0);
    float state_three = get_numeric_state(3);
    if (context_value == 12) {
        if (state_zero == 2) {
            if (state_three == 1) {
                set_primary_flag(24, true);
            }
        }
    }
}
