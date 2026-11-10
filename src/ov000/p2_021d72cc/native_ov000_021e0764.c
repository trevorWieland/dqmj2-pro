#include "context.h"

/* Refresh the two sub-systems that contribute to the current frame cost and
   return their sum. */
s32 native_ov000_021e0764(void)
{
    s32 total = 0;

    native_fn_ov000_021e0654();
    total = total + native_fn_ov000_021e87d4();
    total = total + native_fn_ov000_02210758();
    return total;
}
