typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct Input {
    u16 prefix;
    u16 pressed;
    u16 unknown;
    u16 repeated;
} Input;
typedef struct Selection {
    s8 group;
    s8 previousGroup;
    u8 x;
    u8 y;
    u8 dragging;
    s8 dragIndex;
    u8 pending;
} Selection;
typedef struct Context {
    u8 prefix;
    u8 groupCount;
    u8 unknown[4];
    u8 special;
} Context;
extern Input *native_fn_0202a634(void);
extern void native_fn_0205e7a8(s32 owner, u32 code);
extern u32 native_fn_02069000(void);
extern u32 native_fn_0206ba88(void);
extern u32 native_fn_0206c228(void);
extern s32 native_fn_0206d250(s32 sprite);
extern u32 native_fn_02072918(Selection *selection, void *layout, u32 groups, void *rows);
extern u32 native_fn_02072f0c(void);
extern void native_fn_020c0274(Selection *selection);
extern u32 native_fn_020c1794(void);
extern Context native_data_021c48f8;
extern u8 native_data_021c491a[];
extern u8 native_data_021c491d[];
extern Selection native_data_021c4968;
extern u8 native_data_021c4a04[];
extern u8 native_data_021c4a0b[];
extern s8 native_data_021c4a10[];
u32 native_main_0206940c(void) {
    s32 metric = 0;
    u32 row;
    Input *input = native_fn_0202a634();
    u32 changed = 0;
    if (native_data_021c48f8.special != 0 && native_data_021c4968.group == native_fn_02069000()) {
        native_fn_020c0274(&native_data_021c4968);
        return 0;
    }
    if ((input->repeated & 0xF0) != 0) {
        native_fn_0205e7a8(-1, 0x55);
    }
    if (native_data_021c4968.group == -1) {
        native_fn_02072918(&native_data_021c4968, native_data_021c491a,
            native_data_021c48f8.groupCount, native_data_021c4a04);
        return 0;
    }
    if ((input->repeated & 0x40) != 0) {
        if (native_data_021c4968.y == 0) {
            if (native_data_021c4968.dragging == 0) {
                native_data_021c4968.previousGroup = native_data_021c4968.group;
                native_data_021c4968.group = -1;
                if (native_data_021c4968.previousGroup != native_fn_0206c228() - 1) {
                    native_data_021c4968.x = 0;
                } else {
                    native_data_021c4968.x = native_fn_02072f0c() - 1;
                }
            } else {
                native_data_021c4968.y = 2 - native_fn_0206d250(native_data_021c4a10[native_data_021c4968.dragIndex * 16]);
            }
        } else {
            native_data_021c4968.y--;
            if (native_data_021c4968.dragging == 0) {
                row = native_fn_0206ba88();
                if (row != 0xFFFFFFFF) {
                    native_data_021c4968.y -= native_fn_0206d250(native_data_021c4a10[row * 16]);
                }
            }
        }
        changed = 1;
    } else if ((input->repeated & 0x80) != 0) {
        row = native_fn_0206ba88();
        if (row != 0xFFFFFFFF) {
            metric = native_fn_0206d250(native_data_021c4a10[row * 16]);
        }
        if ((native_data_021c4968.dragging == 0 && native_data_021c4968.y >= 2 - metric) ||
            (native_data_021c4968.dragging != 0 && native_data_021c4968.y >=
                2 - native_fn_0206d250(native_data_021c4a10[native_data_021c4968.dragIndex * 16]))) {
            if (native_data_021c4968.dragging == 0) {
                native_data_021c4968.previousGroup = native_data_021c4968.group;
                native_data_021c4968.group = -1;
                if (native_data_021c4968.previousGroup != native_fn_0206c228() - 1) {
                    native_data_021c4968.x = 0;
                } else {
                    native_data_021c4968.x = native_fn_02072f0c() - 1;
                }
            } else {
                native_data_021c4968.y = 0;
            }
        } else {
            if (native_data_021c4968.dragging == 0 && native_fn_0206ba88() != 0xFFFFFFFF) {
                native_data_021c4968.y += metric;
            }
            native_data_021c4968.y++;
        }
        changed = 1;
    } else if ((input->repeated & 0x20) != 0) {
        if (native_data_021c4968.x == 0) {
            native_data_021c4968.previousGroup = native_data_021c4968.group;
            native_data_021c4968.group--;
            if (native_data_021c4968.group < 0) {
                if (native_data_021c48f8.special == 0 || native_fn_020c1794() != 0) {
                    native_data_021c4968.group += native_data_021c48f8.groupCount;
                } else if (native_data_021c48f8.special != 0) {
                    native_data_021c4968.group = native_fn_02069000();
                    if (native_data_021c4968.dragging == 0) {
                        native_data_021c4968.pending = 1;
                    }
                }
            }
            native_data_021c4968.x = native_data_021c491d[native_data_021c4968.group * 5] - 1;
            if (native_data_021c4968.dragging == 0) {
                row = native_fn_0206ba88();
                if (row != 0xFFFFFFFF) {
                    native_data_021c4968.y = native_data_021c4a0b[row * 16];
                }
            }
        } else {
            native_data_021c4968.x--;
            if (native_data_021c4968.dragging == 0) {
                row = native_fn_0206ba88();
                if (row != 0xFFFFFFFF) {
                    native_data_021c4968.y = native_data_021c4a0b[row * 16];
                }
            }
        }
        changed = 1;
    } else if ((input->repeated & 0x10) != 0) {
        if (native_data_021c4968.x >= native_data_021c491d[native_data_021c4968.group * 5] - 1) {
            native_data_021c4968.previousGroup = native_data_021c4968.group;
            native_data_021c4968.group++;
            native_data_021c4968.x = 0;
            if (native_data_021c4968.group >= native_data_021c48f8.groupCount &&
                (native_data_021c48f8.special == 0 || native_fn_020c1794() != 0)) {
                native_data_021c4968.group = 0;
            }
            if (native_data_021c4968.dragging == 0) {
                row = native_fn_0206ba88();
                if (row != 0xFFFFFFFF) {
                    native_data_021c4968.y = native_data_021c4a0b[row * 16];
                }
            }
        } else {
            native_data_021c4968.x++;
            if (native_data_021c4968.dragging == 0) {
                row = native_fn_0206ba88();
                if (row != 0xFFFFFFFF) {
                    native_data_021c4968.y = native_data_021c4a0b[row * 16];
                }
            }
        }
        changed = 1;
    } else if ((input->pressed & 8) != 0) {
        if (native_data_021c4968.dragging == 0) {
            native_data_021c4968.group = -1;
            native_data_021c4968.x = 0;
            native_data_021c4968.pending = 0;
            native_fn_0205e7a8(-1, 0x55);
        } else {
            native_fn_0205e7a8(-1, 0x54);
        }
    }
    return changed;
}
