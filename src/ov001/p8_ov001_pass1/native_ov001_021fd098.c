#include "context.h"

/* Signed byte at 0x02239c9c indexed by the caller's index plus 0 or 3, selected
 * by the first argument.  The offset is an s8, which is why the image sign
 * extends the conditional value with lsl/asr before the add. */
s8 native_ov001_021fd098(s32 selector, s32 index)
{
    s8 extra = selector == 0 ? 0 : 3;

    return *(s8 *)(native_data_ov001_02239c9c + (index + extra));
}
