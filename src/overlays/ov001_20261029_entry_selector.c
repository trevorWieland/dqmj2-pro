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
extern u32 native_fn_020443ec();
extern u32 native_fn_020444ec();
extern u32 native_fn_0205f210(u32, u32);
extern u32 native_fn_ov001_021dba58(u32, u32);
extern u32 native_fn_ov001_021dbac8(u32);
extern u32 native_fn_ov001_021e35b4(u32);
extern u32 native_fn_ov001_021e36c4(u32, u32, u32, u32, u32);
extern u32 native_fn_ov001_021f112c(u32);
extern u32 native_fn_ov001_021f1294(u32, u32);
extern u32 native_fn_ov001_021f92b8();
extern u32 native_fn_ov001_021f9350(u32);
typedef struct {
    u8 unknown_0[0x2];
    u8 field_2;
    u8 unknown_3[0x13];
    s8 field_16;
} Record_native_data_ov001_02238cd4;
extern Record_native_data_ov001_02238cd4 native_data_ov001_02238cd4;
u32 native_ov001_021e3764(void) {
    u32 temp_r4;
    u32 temp_r4_2;
    u32 temp_r5;
    u32 temp_r6;
    u32 temp_r7;
    u32 temp_r8;
    u32 temp_r9;

    native_fn_ov001_021f112c(2);
    temp_r4 = native_fn_ov001_021dba58(0, 2);
    temp_r6 = native_fn_ov001_021dba58(1, 2);
    temp_r5 = native_fn_ov001_021dba58(0, 1);
    temp_r7 = native_fn_ov001_021dba58(1, 1);
    temp_r8 = native_fn_ov001_021dbac8(0);
    temp_r9 = native_fn_ov001_021dbac8(1);
    if ((native_data_ov001_02238cd4.field_2 != 6) && (native_data_ov001_02238cd4.field_2 != 7)) {
        native_fn_0205f210(1, 1);
    }
    native_fn_ov001_021f92b8();
    if (native_data_ov001_02238cd4.field_2 == 0) {
        native_fn_ov001_021e36c4(0x2A, 7, temp_r8, temp_r4, temp_r5);
        native_fn_ov001_021e35b4(0x14);
        native_fn_ov001_021f9350(0);
        temp_r4_2 = native_fn_020443ec();
        if (native_fn_020444ec() != 0) {
            native_data_ov001_02238cd4.field_16 = 0xD;
        } else {
            if (temp_r4_2 == 5) {
                native_data_ov001_02238cd4.field_16 = 0xD;
            }
            else if (temp_r4_2 == 6) {
                native_data_ov001_02238cd4.field_16 = 0xE;
            }
            else if (temp_r4_2 == 7) {
                native_data_ov001_02238cd4.field_16 = 0x10;
            }
            else {
                native_data_ov001_02238cd4.field_16 = 1;
            }

        }
    }
    else if (native_data_ov001_02238cd4.field_2 == 1) {
        native_fn_ov001_021e36c4(0x2A, 7, temp_r8, temp_r4, temp_r5);
        native_fn_ov001_021e35b4(0x15);
        native_fn_ov001_021f9350(1);
        native_data_ov001_02238cd4.field_16 = 2;
    }
    else if (native_data_ov001_02238cd4.field_2 == 2) {
        native_fn_ov001_021e36c4(0x2A, 0xB, temp_r8, temp_r4, temp_r5);
        native_fn_ov001_021f9350(2);
        native_data_ov001_02238cd4.field_16 = 3;
    }
    else if (native_data_ov001_02238cd4.field_2 == 4) {
        native_data_ov001_02238cd4.field_16 = 4;
    }
    else if (native_data_ov001_02238cd4.field_2 == 3) {
        native_data_ov001_02238cd4.field_16 = 4;
    }
    else if (native_data_ov001_02238cd4.field_2 == 6) {
        native_data_ov001_02238cd4.field_16 = 5;
    }
    else if (native_data_ov001_02238cd4.field_2 == 7) {
        native_data_ov001_02238cd4.field_16 = 6;
    }
    else if (native_data_ov001_02238cd4.field_2 == 8) {
        native_fn_ov001_021e36c4(0x2A, 7, temp_r8, temp_r4, temp_r5);
        native_fn_ov001_021e36c4(0x30, 9, temp_r8, temp_r4, temp_r5);
        native_fn_ov001_021e35b4(0x14);
        native_fn_ov001_021f9350(3);
        native_data_ov001_02238cd4.field_16 = 7;
    }
    else if (native_data_ov001_02238cd4.field_2 == 9) {
        native_fn_ov001_021e36c4(0x2A, 7, temp_r8, temp_r4, temp_r5);
        native_fn_ov001_021e36c4(0x30, 9, temp_r8, temp_r4, temp_r5);
        native_fn_ov001_021e35b4(0x15);
        native_fn_ov001_021f9350(3);
        native_data_ov001_02238cd4.field_16 = 8;
    }
    else if (native_data_ov001_02238cd4.field_2 == 5) {
        native_fn_ov001_021e36c4(0x2A, 7, temp_r8, temp_r4, temp_r5);
        native_fn_ov001_021e36c4(0x30, 9, temp_r8, temp_r4, temp_r5);
        native_fn_ov001_021e35b4(0x14);
        native_fn_ov001_021f9350(3);
        native_data_ov001_02238cd4.field_16 = 9;
    }
    else if (native_data_ov001_02238cd4.field_2 == 10) {
        native_fn_ov001_021e36c4(0x2A, 0xB, temp_r9, temp_r6, temp_r7);
        native_fn_ov001_021e35b4(0x15);
        native_fn_ov001_021f9350(3);
        native_data_ov001_02238cd4.field_16 = 0xA;
    }
    else if (native_data_ov001_02238cd4.field_2 == 11) {
        native_fn_ov001_021e36c4(0x2A, 0xB, temp_r9, temp_r6, temp_r7);
        native_fn_ov001_021e35b4(0x14);
        native_fn_ov001_021f9350(3);
        native_data_ov001_02238cd4.field_16 = 0xB;
    }
    else if (native_data_ov001_02238cd4.field_2 == 12) {
        native_fn_ov001_021e36c4(0x2A, 0xB, temp_r9, temp_r6, temp_r7);
        native_fn_ov001_021e35b4(0x15);
        native_fn_ov001_021f9350(3);
        native_data_ov001_02238cd4.field_16 = 0xC;
    }

    native_fn_ov001_021f1294(0x10, 2);
    return 1U;
}
