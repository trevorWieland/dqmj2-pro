#include "context.h"

/* True while the selection word at 0x02242998+8 is one of the two live modes
 * (0 or 3).  Both comparisons are emitted as a `cmp`/`cmpne` pair, which is what
 * the two ORed equality tests compile to. */
s32 native_ov001_02213b5c(void)
{
    s32 mode = *(s32 *)(native_data_ov001_02242998 + 8);

    return mode == 3 || mode == 0;
}
