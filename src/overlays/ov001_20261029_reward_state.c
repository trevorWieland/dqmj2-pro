typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_0202a634();
extern u32 native_fn_02041510();
extern u32 native_fn_02041800();
extern u32 native_fn_0204437c();
extern u32 native_fn_0204439c();
extern u32 native_fn_02047d40();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_0205eb00();
extern u32 native_fn_0205f210();
extern u32 native_fn_0205f2d8();
extern u32 native_fn_020630e4();
extern u32 native_fn_ov001_021d75d4();
extern u32 native_fn_ov001_021d94cc();
extern u32 native_fn_ov001_021dc8e8();
extern u32 native_fn_ov001_021e3508();
extern u32 native_fn_ov001_021e3564();
extern u32 native_fn_ov001_021e3b34();
extern u32 native_fn_ov001_021e3bd0();
extern u32 native_fn_ov001_021e3be4();
extern u32 native_fn_ov001_021e3f68();
extern u32 native_fn_ov001_021e49d0();
extern u32 native_fn_ov001_021e4b34();
extern u32 native_fn_ov001_021e4c34();
extern u32 native_fn_ov001_021f1354();
extern u32 native_fn_ov001_021f1414();
extern u32 native_fn_ov001_021f1438();
extern u32 native_fn_ov001_021f14a4();
extern u32 native_fn_ov001_021f14c0();
extern u32 native_fn_ov001_021f14e4();
extern u32 native_fn_ov001_021f1a44();
extern u32 native_fn_ov001_021f949c();
extern u32 native_fn_ov001_021f94d8();
extern u32 native_fn_ov001_022023c4();
extern u32 native_fn_ov001_02202654();
extern u32 native_fn_ov001_022068ac();
extern u32 native_fn_ov001_02207058();
extern u32 native_fn_ov001_022071f8();
extern u32 native_fn_ov001_022116d0();
extern u32 native_fn_ov001_02211714();
extern u32 native_fn_ov001_0221175c();
extern u32 native_fn_ov001_02212848();
extern u32 native_fn_ov001_02212858();
extern u32 native_fn_ov001_02213630();
extern u32 native_fn_ov001_022139e8();
extern s8 native_data_ov001_0222ec40[];
typedef struct {
    u8 unknown_0[0x1];
    s8 field_1;
    u8 unknown_2[0x2];
    u8 field_4;
    s8 field_5;
    u8 unknown_6[0x4];
    u8 field_a;
    u8 unknown_b[0xb];
    s8 field_16;
    u8 unknown_17[0xa];
    s8 field_21;
    s8 field_22;
    s8 field_23;
    s8 field_24;
    s8 field_25;
    u8 field_26;
    u8 unknown_27[0x9];
    s32 field_30;
    s32 field_34;
} Record_native_data_ov001_02238cd4;
extern Record_native_data_ov001_02238cd4 native_data_ov001_02238cd4;
extern u16 native_data_ov001_02238d10[];
u32 native_ov001_021e4eb0(void) {
    u32 temp_r0;
    u32 temp_r4;

    temp_r4 = native_fn_0202a634();
    if (native_data_ov001_02238cd4.field_4 == 0) {
        native_fn_ov001_021e3b34();
        native_fn_ov001_021d75d4(0x2A);
        native_fn_ov001_021d94cc(1, 0);
        native_fn_ov001_021e3564(0x14, 1);
        native_fn_ov001_02202654();
        native_fn_ov001_021dc8e8(0);
        native_data_ov001_02238cd4.field_5 = 0;
        native_data_ov001_02238cd4.field_4 = 1U;
    }
    if (native_data_ov001_02238cd4.field_4 == 1) {
        if (native_data_ov001_02238cd4.field_a != 0) {
            native_data_ov001_02238cd4.field_25 = (s8) native_fn_ov001_021e3be4();
            native_data_ov001_02238cd4.field_24 = (s8) native_fn_0205e7a8(-1, 0x3A);
            native_data_ov001_02238cd4.field_23 = 0x14;
            native_data_ov001_02238cd4.field_4 = 3U;
            native_data_ov001_02238cd4.field_21 = 0x12;
            native_fn_ov001_02212858(native_data_ov001_02238cd4.field_24);
        }
    } else if (native_data_ov001_02238cd4.field_4 == 3) {
        if (M2C_FIELD(temp_r4, u16 *, 2) & 0xFF7) {
            native_data_ov001_02238cd4.field_4 = 4U;
        }
    } else if (native_data_ov001_02238cd4.field_4 == 4) {
        if (native_fn_ov001_021e3f68() == 0) {
            native_data_ov001_02238cd4.field_4 = 2U;
        } else {
            native_data_ov001_02238cd4.field_4 = 5U;
        }
    } else if (native_data_ov001_02238cd4.field_4 == 5) {
        native_fn_ov001_021f1354(1, 3, 2, 1);
        native_fn_ov001_021f1414(0);
        native_fn_ov001_021f1438();
        native_fn_02047d40(*(native_data_ov001_02238d10 + (native_data_ov001_02238cd4.field_26)));
        native_fn_020630e4(*(native_data_ov001_02238d10 + (native_data_ov001_02238cd4.field_26)), 1);
        if (native_fn_0205f2d8(native_data_ov001_02238cd4.field_24) == 0) {
            native_fn_ov001_021f94d8(0xB5, 1);
        }
        native_data_ov001_02238cd4.field_1 = 0;
        native_data_ov001_02238cd4.field_4 = 6U;
    } else if (native_data_ov001_02238cd4.field_4 == 6) {
        if (native_fn_ov001_021f14c0() != 0) {
            native_data_ov001_02238cd4.field_4 = 7U;
        }
    } else if (native_data_ov001_02238cd4.field_4 == 7) {
        if (M2C_FIELD(temp_r4, u16 *, 2) & 0xFF7) {
            native_data_ov001_02238cd4.field_4 = 8U;
        }
    }

    if (native_data_ov001_02238cd4.field_4 == 8) {
        if (((u32) native_data_ov001_02238cd4.field_26 >= 2U) || (*(native_data_ov001_02238d10 + ++native_data_ov001_02238cd4.field_26) == 0)) {
            native_data_ov001_02238cd4.field_4 = 0xAU;
        } else {
            native_data_ov001_02238cd4.field_4 = 9U;
            native_data_ov001_02238cd4.field_1 = 0;
        }
        native_fn_ov001_021f14a4();
    } else if (native_data_ov001_02238cd4.field_4 == 9) {
        if (native_fn_ov001_021f14e4() == 0) {
            native_data_ov001_02238cd4.field_4 = 5U;
        }
    } else if (native_data_ov001_02238cd4.field_4 == 10) {
        native_data_ov001_02238cd4.field_4 = 2U;
    } else if (native_data_ov001_02238cd4.field_4 == 2) {
        if ((s32) native_data_ov001_02238cd4.field_21 <= 0) {
            native_fn_ov001_021e3508(native_data_ov001_02238cd4.field_34);
            if ((s32) native_data_ov001_02238cd4.field_30 > 0) {
                native_data_ov001_02238cd4.field_4 = 0xBU;
            } else {
                native_fn_02041510(1, 2, 0x1E);
                native_data_ov001_02238cd4.field_4 = 0xCU;
                native_fn_ov001_022023c4(0x400);
            }
        }
    } else if (native_data_ov001_02238cd4.field_4 == 12) {
        if (native_fn_02041800() != 1) {
            native_data_ov001_02238cd4.field_4 = 0x12U;
            M2C_FIELD((void *) native_fn_ov001_021f1a44(native_data_ov001_02238cd4.field_25), s8 *, 0x23) = 0;
        }
    } else if (native_data_ov001_02238cd4.field_4 == 11) {
        if (native_fn_0205f2d8(native_data_ov001_02238cd4.field_24) == 0) {
            native_fn_ov001_021f949c(0x52, 1);
        }
        native_fn_ov001_022116d0();
        native_fn_ov001_022023c4(0x200);
        native_data_ov001_02238cd4.field_4 = 0xDU;
        native_data_ov001_0222ec40[2] = 1;
    } else if (native_data_ov001_02238cd4.field_4 == 13) {
        if (native_fn_ov001_02213630(native_data_ov001_02238cd4.field_25) == 0) {
            if (native_fn_ov001_021e49d0() != 0) {
                native_data_ov001_02238cd4.field_4 = 0xE;
            } else {
                native_fn_ov001_022071f8();
                native_data_ov001_02238cd4.field_4 = 0xF;
            }
            native_fn_ov001_021e4c34();
            native_fn_ov001_021e4b34();
        } else {
            if ((s32) native_data_ov001_02238cd4.field_23 > 0) {
                native_data_ov001_02238cd4.field_23 = (s8) (native_data_ov001_02238cd4.field_23 - 1);
            } else if (M2C_FIELD(temp_r4, u16 *, 2) & 0xFF7) {
                native_data_ov001_0222ec40[3] = 0;
                native_fn_ov001_02211714(native_data_ov001_02238cd4.field_25);
            }
            if (native_fn_ov001_0221175c(native_data_ov001_02238cd4.field_25) != 0) {
                if (!(native_data_ov001_0222ec40[2] & native_data_ov001_0222ec40[3])) {
                    native_fn_ov001_021f949c(0x119, 1);
                }
                native_data_ov001_0222ec40[2] = (s8) ((native_data_ov001_0222ec40[2] + 1) & native_data_ov001_0222ec40[3]);
            } else {
                native_data_ov001_0222ec40[2] = 1;
            }
        }
    } else if (native_data_ov001_02238cd4.field_4 == 14) {
        temp_r0 = native_fn_ov001_02212848();
        if (M2C_FIELD(temp_r4, u16 *, 2) & 0xFF7) {
            native_data_ov001_02238cd4.field_22 = 1;
        }
        if (((temp_r0 == -1U) || (native_fn_0205eb00() == 0)) && (native_data_ov001_02238cd4.field_22 != 0)) {
            native_fn_ov001_022071f8();
            native_data_ov001_02238cd4.field_4 = 0xFU;
        }
    } else if (native_data_ov001_02238cd4.field_4 == 15) {
        if (M2C_FIELD(temp_r4, u16 *, 2) & 0xFF7) {
            native_data_ov001_02238cd4.field_4 = 0x10U;
        }
    }

    if ((native_data_ov001_02238cd4.field_4 == 0x10) && (native_fn_ov001_02207058() != 0)) {
        native_fn_ov001_022139e8(2);
        native_fn_02041510(1, 2, 0x1E);
        native_fn_0205f210(native_data_ov001_02238cd4.field_24, 0x1E);
        native_fn_ov001_022068ac(0x52);
        native_data_ov001_02238cd4.field_4 = 0x11U;
    }
    if ((native_data_ov001_02238cd4.field_4 == 0x11) && (native_fn_02041800() != 1)) {
        native_data_ov001_02238cd4.field_4 = 0x12U;
        M2C_FIELD((void *) native_fn_ov001_021f1a44(native_data_ov001_02238cd4.field_25), s8 *, 0x23) = 0;
    }
    if ((native_data_ov001_02238cd4.field_4 == 0x12) && (M2C_FIELD((void *) native_fn_ov001_021f1a44(native_data_ov001_02238cd4.field_25), s32 *, 0x1C) == 0)) {
        native_data_ov001_02238cd4.field_4 = 0x13U;
    }
    if (native_data_ov001_02238cd4.field_4 == 0x13) {
        native_fn_ov001_021e3bd0();
        if (native_data_ov001_02238cd4.field_26 != 0) {
            native_fn_ov001_021f14a4();
        }
        native_data_ov001_02238cd4.field_16 = 0x11;
        native_data_ov001_02238cd4.field_4 = 0U;
        native_data_ov001_02238cd4.field_26 = 0U;
    }
    if ((s32) native_data_ov001_02238cd4.field_21 > 0) {
        native_data_ov001_02238cd4.field_21 = (s8) (native_data_ov001_02238cd4.field_21 - 1);
    }
    native_fn_0204437c();
    native_fn_0204439c();
    return 0U;
}
