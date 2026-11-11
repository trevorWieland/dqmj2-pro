#include "context.h"

/* Advance the menu sound state: park the pending id, then run either the
   resume or the restart path before switching the channel table. */
void native_ov006_021e5d90(void)
{
    if (native_fn_ov006_021e65a4() != 0) {
        *(s32 *)(native_data_ov006_0220d108 + 0x08) = -1;
        if (*(s32 *)(native_data_ov006_02218d70 + 0x08) != 0) {
            native_fn_ov006_021e3f28(0x15);
        } else {
            native_fn_ov006_021e7e28();
            native_fn_ov006_021e3f28(2);
        }
    }
    native_fn_ov006_021e3cd8();
}
