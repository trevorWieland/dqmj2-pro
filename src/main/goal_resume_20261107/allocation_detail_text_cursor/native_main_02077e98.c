#include "allocation_detail_text.h"

u32 native_main_02077e98(const SkillSlot *slot, const SkillTable *table, s32 points, s32 preview)
{
    Point position = {0, 0};
    s32 row;
    s32 remaining;
    s32 action;
    u32 cursor;
    u32 separator;

    if (native_data_021c6234.edit_active && preview == 0 &&
        !(native_data_021c6234.current_row == native_data_021c6234.unlocked_row &&
          native_data_021c6234.allocated_points == ((const u8 *)table)[native_data_021c6234.current_row])) {
        row = native_data_021c6234.current_row - 1;
    } else {
        row = native_data_021c6234.current_row;
    }
    native_data_021c6234.highlighted_row = row;
    native_data_021c6234.cached_slot = slot;
    native_data_021c6234.cached_table = table;
    remaining = ((const u8 *)table)[native_data_021c6234.current_row] - points;
    native_fn_02085270(&native_fn_02049ad0(24)->owner->surface->layout, 16, 0);
    position.x = 0;
    if (points != table->thresholds[9] || preview == 0) {
        action = native_fn_0207ad98(table, (s8)row);
        cursor = 32;
        if (native_fn_0207ad80(table, (s8)row)) {
            cursor += native_fn_02048188(cursor, 0);
            cursor += native_fn_0206099c(action, cursor);
            separator = native_fn_02048188(cursor, 2);
            native_fn_02048034(native_fn_0205dc70(7, 0, action), cursor + separator);
        } else {
            separator = native_fn_02048188(cursor, 2);
            cursor += separator;
            native_fn_02048034(native_fn_0205dc70(11, 0, action), cursor);
        }
        if (native_data_021c6234.edit_active == 0 || preview != 0) {
            native_fn_02048094(remaining, 0);
            return native_fn_0204a574(24, &position, 5, 2, 17, 1, 1);
        }
        return native_fn_0204a574(24, &position, 5, 2, 18, 127, 1);
    }
    return native_fn_0204a574(24, &position, 5, 2, 23, 1, 1);
}
