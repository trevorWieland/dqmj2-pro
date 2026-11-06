#include "transfer_narrow_types_20261030.h"
u32 native_main_020c1110(WriterState *saved, BulkSelection *selection, BulkRow *rows, s8 *destination) {
    s32 y;
    s32 target;
    s8 savedIndex;
    s32 groupOffset;
    u32 previousUid;
    s8 sprite;
    BulkRecord *record;
    savedIndex = saved->index;
    if (native_fn_0206c0b0() != 0) {
        target = native_fn_020c0f54(saved->x, saved->y);
        if (target != -1) {
            if (native_fn_020c1794() == 0) {
                groupOffset = native_data_021d4bec.prefix[4] * 6;
                previousUid = native_fn_020bf7e0(target + groupOffset);
                if (previousUid != 0) {
                    sprite = native_data_021d4c0c[native_fn_020bf928(previousUid)];
                    if (native_fn_0206da54((s32)sprite) != 0) {
                        native_fn_0205e7a8(-1, 0x54);
                        return 0xffffffff;
                    }
                    if (native_fn_0206dac8((s32)sprite) != 0 &&
                        native_fn_020c8fa8()->kind == 6 && native_fn_ov000_02227ccc() != 0) {
                        native_fn_0205e7a8(-1, 0x54);
                        return 0xfffffffd;
                    }
                    if (native_fn_0206da90((s32)sprite) != 0 && native_fn_020c8fa8()->kind == 6) {
                        native_fn_0205e7a8(-1, 0x54);
                        return 0xfffffffe;
                    }
                    if (native_fn_0206db00((s32)sprite) != 0 && native_fn_020c8fa8()->kind == 6) {
                        native_fn_0205e7a8(-1, 0x54);
                        return 0xfffffffc;
                    }
                    native_fn_020c0210();
                    native_fn_020bfa38(previousUid);
                    y = rows[savedIndex].y;
                    if (y >= (s32)(2 - native_fn_0206c1a8(native_fn_02062a10(previousUid)->species))) {
                        y = 2 - native_fn_0206c1a8(native_fn_02062a10(previousUid)->species);
                    }
                    record = native_fn_02062a10(previousUid);
                    native_fn_02069330(record, rows[savedIndex].group, rows[savedIndex].x,
                        (u8)y, 0, *native_data_020e2cf0, 15, native_fn_0206c18c(1));
                } else {
                    native_fn_020c0210();
                    rows[savedIndex].enabled = 0;
                    native_fn_020bf990(rows[saved->index].uid, target + groupOffset);
                }
                native_fn_020c06e8((s32)(s8)(*destination - 1), rows, destination, target + groupOffset);
                saved->index = -1;
                native_fn_020c01f0();
                native_data_021d4bec.currentUid = 0;
            } else {
                native_fn_020c0210();
                previousUid = native_fn_020bf7e0(native_data_021d4bec.prefix[4] * 6 + target);
                if (previousUid != 0) {
                    native_fn_020bfa78(previousUid, native_data_021d4bec.currentUid);
                } else {
                    native_fn_020bfa38(native_data_021d4bec.currentUid);
                    native_fn_020bf990(native_data_021d4bec.currentUid, native_data_021d4bec.prefix[4] * 6 + target);
                }
                rows[savedIndex].enabled = 0;
                native_data_021d4bec.currentUid = 0;
                native_fn_020c06e8((s32)(s8)(*destination - 1), rows, destination, 0);
                saved->index = -1;
                native_fn_020c01f0();
            }
            native_fn_0205e7a8(-1, 0x61);
            selection->x = target / 3;
            selection->y = target % 3;
            selection->group = native_fn_02069000();
            return 1;
        }
        if (native_fn_020c1794() != 0) {
            native_fn_020c1484(saved, selection, rows, destination);
        }
        selection->pending = 0;
    }
    return 0;
}
