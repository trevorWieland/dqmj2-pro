#include "../context.h"

/* Picks one live part record from the table selected by `table` (first table at
   0x02236f6c with the count at 0x022355e4+3, second at 0x022362ac with the count
   at +2).  Up to 16 randomly chosen records are tried first; if none is marked at
   +0x31C and reported live by 0x021db8d0, the whole table is scanned in order.
   Returns the record pointer, or NULL when the table has no live record. */
u8 *native_ov001_021db918(u32 table) {
    u8 *base;
    u8 *found;
    u8 *record;
    s32 limit;
    s32 index;
    s32 i;
    s32 tries;

    found = 0;
    base = (table == 0) ? (u8 *)native_data_ov001_02236f6c : (u8 *)native_data_ov001_022362ac;
    limit = (table == 0) ? *(u8 *)(native_data_ov001_022355e4 + 3) : *(u8 *)(native_data_ov001_022355e4 + 2);
    tries = 0;
    do {
        index = native_fn_0203d294(limit) * 1088;
        if (base[index + 0x31C] != 0) {
            if (native_fn_ov001_021db8d0(base + index) != 0) {
                found = base + index;
                break;
            }
        }
        tries++;
    } while (tries < 16);
    if (found == 0) {
        i = 0;
        if (limit > 0) {
            record = base;
            do {
                if (record[0x31C] != 0) {
                    if (native_fn_ov001_021db8d0(record) != 0) {
                        found = base + i * 1088;
                        break;
                    }
                }
                i++;
                record += 1088;
            } while (i < limit);
        }
    }
    return found;
}
