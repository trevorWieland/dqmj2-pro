#include "scr_world_state.h"
extern float cached_numeric_twenty;
extern float cached_numeric_twenty_eight;
extern bool cached_primary_236;
void advance_world_numeric_state(void)
{
    cached_numeric_twenty = get_numeric_state(20);
    cached_numeric_twenty_eight = get_numeric_state(28);
    cached_primary_236 = get_primary_flag(236);
    float state = get_numeric_state(0);
    if (state == 1) {
        state = get_numeric_state(4);
        if (state == 15) {
            set_numeric_state(0, 2);
            set_numeric_state(4, 0);
            set_primary_flag(8, true);
        }
    } else {
        if (state == 3) {
            state = get_numeric_state(4);
            if (state == 1) {
                set_numeric_state(4, 2);
                set_primary_flag(8, true);
            }
            state = get_numeric_state(5);
            if (state == 7) {
                set_numeric_state(5, 8);
            }
        }
    }
    if (cached_numeric_twenty >= 28) {
        bool primary_218 = get_primary_flag(218);
        if (primary_218 == true) {
            state = get_numeric_state(28);
            if (state == 5) {
                set_primary_flag(237, true);
                set_primary_flag(203, false);
            }
        }
    }
}
