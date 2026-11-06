#include "scr_decision.h"
void clear_primary_4_if_set(void)
{
    bool was_set = get_primary_flag(4);
    if (was_set == true) {
        set_primary_flag(4, false);
    }
}
