#include "../context.h"

/* Same walk as 0x021d908c but the result byte is read from the fixed table at
   0x02232b90 with a 9-byte stride and there is no caller-supplied base. */
u32 native_ov001_021d90c4(u32 index, s32 sign) {
    if (sign > 0) {
        index = *(u32 *)(native_data_ov001_0222ea30 + index * 8);
    } else if (sign < 0) {
        index = *(u32 *)(native_data_ov001_0222ea34 + index * 8);
    }
    return native_data_ov001_02232b90[index * 9];
}
