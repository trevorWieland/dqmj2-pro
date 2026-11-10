#include "../context.h"

/* Copies the record's 12-byte vector at +4 into the staging vector at
   0x0222fd2c, optionally rebuilds an empty vector through 0x0202859c, then copies
   the (possibly rebuilt) vector back into the record.  Only kind-0 records take
   part; the return value is the staging address, which doubles as "true", or 0
   when the record is not a kind-0 record. */
u32 native_ov001_021d7d58(u32 slotId, u8 *vector) {
    u8 *record;
    u32 result;

    record = native_data_ov001_0222fda0 + slotId * 0x78;
    result = 0;
    if (record[1] == 0) {
        *(Vector3 *)native_data_ov001_0222fd2c = *(Vector3 *)(record + 4);
        if (vector == 0) {
            vector = native_fn_0202859c(0, 0);
        }
        *(Vector3 *)(record + 4) = *(Vector3 *)vector;
        result = (u32)native_data_ov001_0222fd2c;
    }
    return result;
}
