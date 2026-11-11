/*
 * ov001 packet p4d: accessor-shaped routines from the low end of unit
 * ov001-u2 (0x021e3370-0x021f8fd8). All offsets are measured from the
 * overlay image; no meaning is invented beyond the observed loads, stores
 * and call contracts.
 */
#include "context.h"

extern u32 native_fn_020443ec(void);

/* 0x021e3370: load the parameter block for a slot and hand it to the setup pair. */
void native_ov001_021e3370(void) {
    u32 flag = native_fn_ov001_021dba58(0, 2) != 0;
    u32 *params = (u32 *)native_fn_ov001_021d8b4c(flag, 0);
    u8 *slot = native_fn_ov001_021d8b78(flag);

    native_fn_ov001_021e33c8(params[0], params[1], params[2]);
    native_fn_ov001_021e3408(slot);
    native_fn_ov001_021d95b0(native_data_ov001_02238ad4);
}

/* 0x021e3438: copy the three-word selection block when both gate bytes are set. */
u32 native_ov001_021e3438(void) {
    Params local;
    u32 result = 0;

    if (native_data_ov001_02238ad4[0x1e8] != 0 && native_data_ov001_02238ad4[0x1e9] != 0) {
        if (native_fn_02042b3c(native_data_ov001_02238ad4, &local) != 0) {
            *(Params *)native_data_ov001_02238b44 = local;
            native_fn_ov001_021d95b0(native_data_ov001_02238ad4);
            result = 1;
        }
    }
    return result;
}

/* 0x021e86cc: look up a byte pair and report whether its row is past the cursor. */
u32 native_ov001_021e86cc(u32 arg0, s32 a, s32 b) {
    s32 i = 0;
    do {
        if (((PairEntry *)native_data_ov001_02238d40)[i].a == a &&
            ((PairEntry *)native_data_ov001_02238d40)[i].b == b) {
            return i > (s32)arg0;
        }
        i++;
    } while (i < 6);
    return 0;
}

/* 0x021e9da4: clear the ten slot words that the probe rejects. */
void native_ov001_021e9da4(void) {
    s32 i = 0;
    do {
        u32 value = ((u32 *)native_data_ov001_02238dec)[i];
        if (value != 0xFFFFFFFF && native_fn_0205d6f4(value) == 0) {
            ((u32 *)native_data_ov001_02238dec)[i] = 0xFFFFFFFF;
        }
        i++;
    } while (i < 10);
}

/* 0x021eef20: hand the nineteen table halfwords to the per-entry handler. */
void native_ov001_021eef20(void) {
    s32 i = 0;
    do {
        native_fn_ov001_021eeb70(((u16 *)native_data_ov001_0222ec88)[i]);
        i++;
    } while (i < 19);
}

/* 0x021f0f60: seed the four work words with the caller's value. */
void native_ov001_021f0f60(u32 value) {
    s8 i = 0;
    do {
        ((u32 *)native_data_ov001_02238f6c)[i] = value;
        i++;
    } while (i < 4);
}

/* 0x021f106c: classify the current mode against the 2 and 8 sentinels. */
u32 native_ov001_021f106c(void) {
    u32 value = native_fn_020443ec();
    return value == 2 || value == 8;
}

/* 0x021f307c: report whether the record qualifies for the shared handler. */
u32 native_ov001_021f307c(u8 *arg0, u32 arg1) {
    u8 *record = native_fn_0207afec(arg1);
    if (arg0[0x31c] != 0 && arg0[0x1ff] != 0) {
        if ((((u32)*(u16 *)(record + 8) << 20) >> 28) == 3 || arg1 == 56 || arg1 == 163) {
            return 1;
        }
    }
    return 0;
}

/* 0x021f3470: map the mode selector onto the two accepted state groups. */
u32 native_ov001_021f3470(s32 arg0) {
    if (arg0 < 0) {
        arg0 = (s32)native_fn_ov001_021d767c();
    }
    switch (arg0) {
    case 16:
    case 17:
    case 18:
    case 23:
    case 24:
    case 25:
        return 1;
    default:
        return 0;
    }
}

/* 0x021f8dcc: run the selection handler and reset the byte it reports on. */
u32 native_ov001_021f8dcc(void) {
    u32 flag = native_data_ov001_0223989c[0x35] == 1;
    if (native_fn_ov001_02216ac4(*(u32 *)(native_data_ov001_0223989c + 0x84),
                                 native_data_ov001_0223989c[0x12], flag) != 0) {
        native_data_ov001_0223989c[0x1b] = 27;
    }
    return 0;
}
