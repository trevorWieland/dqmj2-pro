#include "context.h"
u32 native_ov001_021ea56c(void) {
    u32 draw8;
    u32 draw2;
    u32 draw4;
    u32 slot;
    u8 *candidate;
    s8 changedSlot;
    s32 mark;
    s32 rule, available, required;
    u8 *actor;
    s32 side;
    u8 *selected;

    mark = 0;
    native_fn_ov001_021e9cbc();
    if (((u32) (M2C_FIELD((void *) native_fn_0207afec((s32) M2C_FIELD(native_data_ov001_02238d7c, u16 *, 0x36)), u16 *, 8) << 0x18) >> 0x1C) == 3) {
        if (native_fn_02044cdc(M2C_FIELD(M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60), void **, 0x1E8), s16 *, 0x2A)) == 0) {
            draw8 = native_fn_0203d294(8);
            if (M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60), u8 *, 0x31E) == 0) {
                if ((s32) draw8 < 3) {
                    side = 1;
                } else {
                    side = 0;
                }
            } else if ((s32) draw8 < 3) {
                side = 0;
            } else {
                side = 1;
            }
        } else if (native_fn_02044cdc(M2C_FIELD(M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60), void **, 0x1E8), s16 *, 0x2A)) == 1) {
            draw2 = native_fn_0203d294(2);
            if (M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60), u8 *, 0x31E) == 0) {
                if (draw2 == 0) {
                    side = 1;
                } else {
                    side = 0;
                }
            } else if (draw2 == 0) {
                side = 0;
            } else {
                side = 1;
            }
        } else {
            draw4 = native_fn_0203d294(4);
            if (M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60), u8 *, 0x31E) == 0) {
                if (draw4 == 0) {
                    side = 1;
                } else {
                    side = 0;
                }
            } else if (draw4 == 0) {
                side = 0;
            } else {
                side = 1;
            }
        }
        do {
            candidate = native_fn_ov001_021db438(side, native_fn_0203d294(3));
        } while (native_fn_ov001_021db8d0(candidate) == 0);
        M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x54) = candidate;
    }
    if (M2C_FIELD(native_data_ov001_02238d7c, u8 *, 0x1E) == 1) {
        required = 0;
    } else {
        actor = M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60);
        required = native_fn_0207b244(M2C_FIELD(native_data_ov001_02238d7c, u16 *, 0x36), native_fn_ov001_021dbd30(actor), M2C_FIELD(actor, s32 *, 0x1E8) + 0x46);
    }
    available = native_fn_ov001_021dbd30(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60));
    if (M2C_FIELD(native_data_ov001_02238d7c, s8 *, 0x29) == -1) {
        M2C_FIELD(native_data_ov001_02238d7c, s8 *, 0x29) = (s8) native_fn_ov001_021f1414(M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60), u8 *, 0x31E));
    }
    rule = native_fn_ov001_0220f9a4(M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60), void **, 0x1E8) + 0x46, M2C_FIELD(native_data_ov001_02238d7c, u16 *, 0x36), native_data_ov001_02238d8e);
    if ((available >= (s32) required) && (rule == 0)) {
        native_fn_ov001_021db834(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60), (s32) required);
        native_fn_ov001_022024d4(M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60), u8 *, 0x31E), M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60), u8 *, 0x31F), 0);
    }
    if ((M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60), s8 *, 0x255) != 0) && (native_fn_0207b004(M2C_FIELD(native_data_ov001_02238d7c, u16 *, 0x36), 0x02000000) != 0) && (M2C_FIELD(native_data_ov001_02238d7c, u8 *, 0x1E) != 1)) {
        M2C_FIELD(native_data_ov001_02238d7c, s8 *, 0x13) = 0xF;
    } else if (available < (s32) required) {
        M2C_FIELD(native_data_ov001_02238d7c, s8 *, 0x13) = 0x10;
    } else if (rule != 0) {
        M2C_FIELD(native_data_ov001_02238d7c, s8 *, 0x13) = 0xE;
    } else if (M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60), u8 *, 0x31E) == M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x54), u8 *, 0x31E)) {
        M2C_FIELD(native_data_ov001_02238d7c, s8 *, 0x13) = 3;
    } else if (((u32) (M2C_FIELD((void *) native_fn_0207afec((s32) M2C_FIELD(native_data_ov001_02238d7c, u16 *, 0x36)), u16 *, 8) << 0x10) >> 0x1C) == 1) {
        M2C_FIELD(native_data_ov001_02238d7c, s8 *, 0x13) = 3;
        mark = 1;
    } else if (M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60), s8 *, 0x236) != 0) {
        M2C_FIELD(native_data_ov001_02238d7c, s8 *, 0x13) = 3;
        mark = 1;
    } else if (native_fn_ov001_021db9f4(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60)) != 0) {
        M2C_FIELD(native_data_ov001_02238d7c, s8 *, 0x13) = 7;
    } else if ((M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60), u8 *, 0x1FD) != 0) && (M2C_FIELD((void *) native_fn_02065d88(), u8 *, 0x2D) == 4) && ((M2C_FIELD(native_data_ov001_02238d7c, u16 *, 0x36) == 0) || ((u32) (u16) (M2C_FIELD(native_data_ov001_02238d7c, u16 *, 0x36) + 0xFF35) <= 1U)) && (M2C_FIELD(native_data_ov001_02238d7c, u8 *, 0x14) == 0)) {
        M2C_FIELD(native_data_ov001_02238d7c, s8 *, 0x13) = 3;
        mark = 1;
    } else if (M2C_FIELD((void *) native_fn_0207afec((s32) M2C_FIELD(native_data_ov001_02238d7c, u16 *, 0x36)), s16 *, 0xA) != 0) {
        M2C_FIELD(native_data_ov001_02238d7c, s8 *, 0x13) = 1;
    } else {
        slot = native_fn_ov001_021f2304(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x54), M2C_FIELD(native_data_ov001_02238d7c, u16 *, 0x36), M2C_FIELD(native_data_ov001_02238d7c, u8 *, 0x19));
        selected = M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x54);
        if (slot != M2C_FIELD(selected, u8 *, 0x31F)) {
            changedSlot = 1;
        } else {
            changedSlot = 0;
        }
        M2C_FIELD(native_data_ov001_02238d7c, s8 *, 0x1D) = changedSlot;
        M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x54) = native_fn_ov001_021db438((s32) M2C_FIELD(selected, u8 *, 0x31E), slot);
        M2C_FIELD(native_data_ov001_02238d7c, s8 *, 0x13) = 2;
    }
    if (*native_data_ov001_0222ec84 != 0) {
        native_fn_ov001_021f1294(0x10, 2);
    }
    native_fn_ov001_021e1358(M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x54), u8 *, 0x31E));
    if (mark == 0) {
        M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60), s8 *, 0x356) = (s8) native_fn_ov001_021f0bec(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60));
    } else {
        M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60), s8 *, 0x356) = 1;
    }
    M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60), s16 *, 0x346) = (s16) native_fn_ov001_021f0c40(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60));
    native_fn_02008d78(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60) + 0x34E, 0, 6);
    if (native_fn_ov001_021e19c8() == 0) {
        native_fn_ov001_02202568(M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60), u8 *, 0x31E), M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, u8 **, 0x60), u8 *, 0x31F));
    }
    M2C_FIELD(native_data_ov001_02238d7c, s8 *, 0xA) = 0;
    return 1U;
}
