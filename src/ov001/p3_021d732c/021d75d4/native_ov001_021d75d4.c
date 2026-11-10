#include "../context.h"

/* Selects a roster record by slot id and resets its action state.  A slot id of
   -1 means "the currently selected record" (0x0222fd50.field_4c).  Selecting
   stores the id back into the 0x4C cell and returns the previously selected id,
   or -1 when the id is out of range or the record is unoccupied.  Kind 2 records
   have their +0x1C action state re-armed and their per-kind callback refreshed;
   kind 1 records only clear the 0x10-byte block at +0x20. */
u32 native_ov001_021d75d4(u32 slotId) {
    s32 previous;
    u32 index;
    s32 offset;
    u8 *record;

    previous = -1;
    index = (u8)slotId;
    if (index < 0x31) {
        offset = slotId * 0x78;
        record = native_data_ov001_0222fda0 + offset;
        if (native_data_ov001_0222fda0[offset] != 0) {
            previous = native_data_ov001_0222fd50.field_4c;
            native_data_ov001_0222fd50.field_4c = (s16)index;
            if (record[1] == 2) {
                native_fn_020448b8(record + 0x1C);
                native_fn_02044988(record + 0x1C, 0);
                native_fn_02044978(record + 0x1C, 0, 0, 0);
                native_fn_ov001_021d768c(slotId);
            } else if (record[1] == 1) {
                native_fn_02008d78(record + 0x20, 0, 0x10);
            }
        }
    }
    return previous;
}
