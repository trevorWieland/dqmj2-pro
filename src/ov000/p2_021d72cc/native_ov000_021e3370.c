#include "context.h"

/* Clear a slot's one-byte state word through the shared teardown, leaving
   negative (already released) slots alone. */
void native_ov000_021e3370(s32 index)
{
    if (native_data_ov000_022322d0[index] < 0)
        return;
    native_fn_0205d718();
    native_data_ov000_022322d0[index] = -1;
}
