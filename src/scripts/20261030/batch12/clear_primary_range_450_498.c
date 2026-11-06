#include "scr_runtime_flags.h"
void clear_primary_range_450_498(void)
{
    for (int flag = 450; flag < 499; ++flag) {
        set_primary_flag(flag, false);
    }
}
