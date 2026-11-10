#include "../context.h"

/* Second staging path of 0x021d7d58's kind-0 family: it stages the record's
   12-byte vector at +0x10 through
   0x0222fd38 and rebuilds a missing vector through 0x020285c8. */
u32 native_ov001_021d7dc4(u32 slotId, u8 *vector) {
    u8 *record;
    u32 result;

    record = native_data_ov001_0222fda0 + slotId * 0x78;
    result = 0;
    if (record[1] == 0) {
        *(Vector3 *)native_data_ov001_0222fd38 = *(Vector3 *)(record + 0x10);
        if (vector == 0) {
            vector = native_fn_020285c8(0, 0);
        }
        *(Vector3 *)(record + 0x10) = *(Vector3 *)vector;
        result = (u32)native_data_ov001_0222fd38;
    }
    return result;
}

