#include "context.h"

/* Drop the referenced record and clear the owning slot. */
void native_main_02038100(u32 *volatile *slot)
{
    if (*slot == 0)
        return;
    *(*slot) = 0;
    *slot = 0;
}

