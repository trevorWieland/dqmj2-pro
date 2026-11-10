#include "context.h"

/* True for the two "no request" selector values.  The first parameter is
   carried by the caller's ABI and is not read. */
u32 native_main_021d7240(u32 unused, u32 selector)
{
    return selector == 0 || selector == 2;
}
