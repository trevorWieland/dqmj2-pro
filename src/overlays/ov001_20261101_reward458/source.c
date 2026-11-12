#include "context.h"
u32 native_ov001_021e3f68(void) {
    s32 index;
    u8 *actor;
    u32 any;
    s32 count;
    u8 *flags, *descriptor;
    u32 ready, item;
    count = 0;
    any = 0;
    native_fn_02008d78(native_data_ov001_02238d10, 0, 6);
    flags = native_data_ov001_02238d18;
    index = 0;
    do {
        actor = ov001_side_slot_record_021db438(1, index);
        ready = actor[0x31C];
        if (ready != 0 && actor[0x1FF] != 0) {
            item = native_fn_ov001_021e3eec(actor, 0);
            if (item != 0) {
                any = 1;
                native_data_ov001_02238d10[count] = item;
                ++count;
            }
        } else if (*flags != 0 && ready != 0 && (descriptor = *(u8 **)(actor + 0x1E8), descriptor[0xAC] != 0)) {
            if (native_fn_ov001_021e3db0(descriptor[0xD0], 0, 0) != 0) {
                item = *(u16 *)(*(u8 **)(actor + 0x1E8) + 0xCE);
                any = 1;
                native_data_ov001_02238d10[count] = item;
                ++count;
            }
        }
        ++index;
        ++flags;
    } while (index < 3);
    return any;
}
