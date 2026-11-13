#include "../context.h"

/* Counts the live records of one part table and reports the total.  The kind
   selects both the table base (0x02236f6c, 0x022362ac, 0x022355ec or
   0x02237c2c for any other kind) and one of the four counts held in the
   0x022355e4 block; records are 1088 bytes apart and are live when 0x021db8d0
   reports them so. */
u32 native_ov001_021db578(u32 kind) {
    s32 i;
    u32 count;
    s32 limit;
    u8 *record;

    if (kind == 0) {
        limit = *(u8 *)(native_data_ov001_022355e4 + 3);
        record = (u8 *)native_data_ov001_02236f6c;
    } else if (kind == 1) {
        limit = *(u8 *)(native_data_ov001_022355e4 + 2);
        record = (u8 *)native_data_ov001_022362ac;
    } else if (kind == 2) {
        limit = *(u8 *)native_data_ov001_022355e4;
        record = (u8 *)native_data_ov001_022355ec;
    } else {
        limit = *(u8 *)(native_data_ov001_022355e4 + 1);
        record = (u8 *)native_data_ov001_02237c2c;
    }
    i = 0;
    count = 0;
    while (i < limit) {
        if (ov001_record_is_active_021db8d0(record) != 0) {
            count++;
        }
        i++;
        record += 1088;
    }
    return count;
}



