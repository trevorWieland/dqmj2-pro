#include "placement_caller_types_20261030.h"
void native_main_020c09f4(s32 index, u32 group, u32 x, u32 y, BulkRow *rows, s8 *count) {
    s32 position;
    native_data_021d4bec.currentUid = 0;
    native_fn_020c0210();
    rows[index].group = group;
    rows[index].x = x;
    rows[index].y = y;
    rows[index].flagA = 0;
    position = native_fn_020bf8c8(rows[index].uid);
    native_fn_020bfa38(rows[index].uid);
    native_fn_020c06e8(index, rows, count, (u32)position);
    native_fn_0206c2f8();
    native_fn_020c01f0();
}
