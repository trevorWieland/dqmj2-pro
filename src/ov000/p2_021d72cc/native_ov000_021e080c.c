#include "context.h"

/* Open the shared session when the stored state word is not already released.
   Reports whether the open call ran. */
s32 native_ov000_021e080c(s32 value)
{
    s32 opened = 0;

    if (native_data_ov000_022322d0[0] >= 0) {
        native_fn_0205ce38(native_data_ov000_022322d0[0], value);
        opened = 1;
    }
    return opened;
}
