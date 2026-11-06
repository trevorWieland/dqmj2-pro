#include "state_writer_types_20261030.h"
void native_main_020c1484(WriterState *saved, BulkSelection *selection, BulkRow *rows, s8 *destination) {
    s8 index;
    s32 position;
    s32 relative;
    index = saved->index;
    native_fn_020c0210();
    rows[index].enabled = 0;
    position = native_fn_020bf8c8(native_data_021d4bec.currentUid);
    relative = position % 6;
    selection->x = relative / 3;
    selection->y = relative % 3;
    selection->group = native_fn_02069000();
    native_data_021d4bec.currentUid = 0;
    native_fn_020c06e8((s32)(s8)(*destination - 1), rows, destination, 0);
    saved->index = -1;
    native_fn_020c01f0();
}
