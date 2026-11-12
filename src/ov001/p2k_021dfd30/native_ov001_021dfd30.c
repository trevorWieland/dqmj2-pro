#include "context.h"

/* Register the caller's handler value in the first free slot of the six-slot
 * table. */
void native_ov001_021dfd30(void)
{
    s32 value = ov001_side_slot_record_021db438();
    s32 index;

    if (ov001_record_is_active_021db8d0() == 0)
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
