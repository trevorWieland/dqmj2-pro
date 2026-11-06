#include "scr_flags.h"
void clear_primary_flags_281_through_284(void)
{
    for (int flag = 281; flag < 285; ++flag) {
        set_primary_flag(flag, false);
    }
}
