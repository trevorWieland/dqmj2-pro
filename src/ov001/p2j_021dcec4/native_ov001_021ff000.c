#include "context.h"

/* Play the caller's sequence on the current sound handle, at the power-on or
 * the looped entry point depending on the selection flag. */
void native_ov001_021ff000(s32 arg0, s32 arg1)
{
    s32 entry = 9;

    if (arg1 != 0)
        entry = 0xC;
    native_fn_0206c718(*(s32 *)(native_data_ov001_02239c10 + 0x24), 1, arg0, arg1, 0, entry);
}
