#include "context.h"

/* Register the caller's handler value in the first free slot of the six-slot
 * table. */
void native_ov001_021dfd30(void)
{
    s32 value = native_fn_ov001_021db438();
    s32 index;

    if (native_fn_ov001_021db8d0() == 0)
        return;
    index = 0;
    do {
        if (*(s32 *)(native_data_02238950 + index * 4) == 0) {
            *(s32 *)(native_data_02238950 + index * 4) = value;
            return;
        }
        index++;
        if (index >= 6)
            return;
    } while (1);
}
