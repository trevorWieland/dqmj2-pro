#include "scr_calls.h"
void clear_primary_flags_after_hook(void)
{
    before_primary_flag_reset();
    for (int flag = 281; flag < 285; ++flag) {
        set_primary_flag(flag, false);
    }
}
