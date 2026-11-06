#include "context.h"
void native_ov000_021ec308(s32 tag)
{
    s8 index;
    for (index = 0; index < 9; index++) {
        u8 *object;
        object = native_fn_main_02049ad0(index);
        if (*(s8 *) (object + 4) == tag)
            native_fn_ov000_021ec348(index);
    }
}
