#include "navigation_types_20261030.h"
extern Input *native_fn_0202a634(void);
extern void native_fn_0205e7a8(s32 owner, u32 code);
extern u32 native_fn_02069000(void);
extern u32 native_fn_0206ba88(void);
extern u32 native_fn_0206c228(void);
extern s32 native_fn_0206d250(s32 sprite);
extern u32 native_fn_020bf6c4(void);
extern void native_fn_020c17e8(s32 index, u32 mode);
extern u8 native_data_021c5a10[];
extern u8 native_data_021c5a19[];
u32 native_main_02072918(Selection *selection, void *layout, u32 groups, Row *rows) {
    Input *input = native_fn_0202a634();
    u8 x = selection->x;
    u32 found = 0;
    u32 selected;
    if (native_data_021c5a19[x * 9] == 0) {
        if ((input->repeated & 0x40) != 0) {
            if (x == 0) {
                selection->group = 0;
                selection->x = 0;
            } else {
                selection->group = native_fn_0206c228() - 1;
                if (selection->group != native_fn_02069000()) {
                    selection->x = 0;
                } else {
                    selection->x = 1;
                    native_fn_020c17e8(native_fn_020bf6c4() - 1, 1);
                }
            }
            selection->previousGroup = -1;
            if (selection->dragging == 0) {
                selection->y = 2;
                selected = native_fn_0206ba88();
                if (selected != 0xFFFFFFFF) {
                    found = 1;
                    selection->y = rows[selected].y;
                }
            } else {
                selection->y = 2 - native_fn_0206d250(rows[selection->dragIndex].sprite);
            }
        } else if ((input->repeated & 0x80) != 0) {
            if (x == 0) {
                selection->group = 0;
                selection->x = 0;
                selection->previousGroup = -1;
            } else {
                selection->group = native_fn_0206c228() - 1;
                selection->x = 0;
                if (selection->group == native_fn_02069000()) {
                    native_fn_020c17e8(0, 1);
                }
            }
            selection->y = 0;
            if (native_fn_0206ba88() != 0xFFFFFFFF) {
                found = 1;
            }
        } else if ((input->repeated & 0x20) != 0) {
            if (x != 0) {
                selection->x = x - 1;
            } else {
                selection->x = *native_data_021c5a10 - 1;
            }
        } else if ((input->repeated & 0x10) != 0) {
            selection->x = x + 1;
            if (selection->x > *native_data_021c5a10 - 1) {
                selection->x = 0;
            }
        } else if ((input->pressed & 8) != 0) {
            selection->x = 0;
            native_fn_0205e7a8(-1, 0x55);
        }
    }
    native_data_021c5a19[selection->x * 9] = 0;
    return found;
}
