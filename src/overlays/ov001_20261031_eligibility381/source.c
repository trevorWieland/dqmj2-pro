#include "context.h"
u32 native_ov001_02209c34(void) {
    u32 ids[3];
    u8 count;
    u8 index;
    void *actor;
    native_fn_0206bc80(ids, &count);
    index = 0;
    if ((u32)count > (u32)index) {
        do {
            actor = (void *)native_fn_ov001_021dc2f8(ids[index]);
            if (actor && native_fn_ov001_021db8d0(actor)) return 1;
            if (native_data_ov001_0223def8.field_1c == ids[index]) return 1;
            index++;
        } while (index < count);
    }
    return 0;
}
