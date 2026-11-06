#include "scr_numeric.h"
void advance_numeric_nine_when_values_match(void)
{
    float context_value = get_context_value(0);
    float state_zero = get_numeric_state(0);
    float state_nine = get_numeric_state(9);
    if (context_value == 60) {
        if (state_zero == 7) {
            if (state_nine == 2) {
                set_numeric_state(9, 3);
            }
        }
    }
}
