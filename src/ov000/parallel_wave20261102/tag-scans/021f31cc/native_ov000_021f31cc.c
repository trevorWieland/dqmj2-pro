#include "context.h"
void native_ov000_021f31cc(s32 tag)
{
    s8 index;
    for (index = 0; index < 19; index++) {
        u8 *object;
        object = native_fn_main_02049ad0(index);
        if (*(s8 *) (object + 4) == tag)
            native_fn_ov000_021f320c(index);
    }
}
