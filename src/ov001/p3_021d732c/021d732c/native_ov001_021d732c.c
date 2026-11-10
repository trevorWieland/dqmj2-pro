#include "../context.h"

/* Claims record `slotId` of the 0x78-byte table at 0x0222fda0 and stores `value`
   in the record's second byte.  The occupancy guard folds the id to its low byte
   (ids are packed as u8) while the record offset keeps the caller's full word,
   which is the arithmetic the original performs.  Returns 1 when this call took
   the record, 0 when it was already claimed or the id is out of range. */
u32 native_ov001_021d732c(u32 slotId, u32 value) {
    u32 claimed = 0;
    u8 *record;

    if ((u8)slotId < 0x31) {
        record = native_data_ov001_0222fda0 + slotId * 0x78;
        if (*record == 0) {
            claimed = 1;
            *record = 1;
            record[1] = (u8)value;
        }
    }
    return claimed;
}
