#define NULL ((void *)0)
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
extern u32 native_fn_02045dc4();
extern u32 native_fn_02049008();
extern u32 native_fn_02049ad0();
extern u32 native_fn_0206006c();
extern u32 native_fn_0206db90();
extern u32 native_fn_020851d4();
extern u32 native_fn_ov000_0221ca80();
extern u32 native_fn_ov000_0221cc08();
extern u32 native_fn_ov000_0221ef90();
extern u32 native_fn_ov000_0221f114();
extern u32 native_fn_ov000_0221fce0();
extern u32 native_fn_ov000_022202f4();
extern u32 native_fn_ov000_02220be8();
extern u32 native_fn_ov000_02220ed4();
extern u32 native_fn_ov000_02221118();
extern u32 native_fn_ov000_02221134();
typedef struct {
    u8 unknown_0[0x2];
    s8 field_2;
    s8 field_3;
    s8 field_4;
} Record_native_data_ov000_022461c4;
extern Record_native_data_ov000_022461c4 native_data_ov000_022461c4;
typedef struct {
    u8 unknown_0[0x1];
    u8 field_1;
    u8 unknown_2[0x3];
    u8 field_5;
    u8 field_6;
    u8 unknown_7[0x3];
    u8 field_a;
    u8 field_b;
    u8 field_c;
    u8 unknown_d[0x3];
    u8 field_10;
    u8 unknown_11[0xe];
    u8 field_1f;
} Record_native_data_ov000_022461f8;
extern Record_native_data_ov000_022461f8 native_data_ov000_022461f8;
extern u8 native_data_ov000_0224621c[];
u32 native_ov000_0221d110(void *arg0, s32 arg1, u32 arg2) {
    s8 temp_r0_3;
    s8 temp_r0_4;
    u32 temp_r0_2;
    u8 *temp_r0;
    s8 temp_r3;
    void *temp_r3_2;
    s8 var_r7;
    void *temp_r8;
    s32 sp8;

    temp_r3 = M2C_FIELD(arg0, s8 *, 0x10);
    sp8 = arg1;
    if (temp_r3 == 1) {
        native_fn_ov000_02221134();
    } else if (temp_r3 != 8) {
        if ((native_data_ov000_022461f8.field_5 == 0) && (native_data_ov000_022461f8.field_6 == 0)) {
            native_fn_02049008(arg0, native_data_ov000_022461c4.field_2, native_data_ov000_022461c4.field_3, native_data_ov000_022461c4.field_4, 2);
        }
    } else {
        native_fn_ov000_0221f114();
    }
    var_r7 = 0;
    do {
        temp_r0 = native_fn_02049ad0(var_r7);
        temp_r8 = M2C_FIELD(temp_r0, void **, 0);
        if ((temp_r8 != NULL) && ((M2C_FIELD(M2C_FIELD(temp_r8, void **, 4), s32 *, 0x18) & 2) == 2)) {
            temp_r0_2 = native_fn_0206db90(M2C_FIELD(temp_r0, s8 *, 5));
            if (temp_r0_2 != 0x7F) {
                temp_r3_2 = M2C_FIELD(temp_r8, void **, 4);
                if (M2C_FIELD(temp_r0, s8 *, 5) == 0x7F) {
                    native_fn_02045dc4(1, 1, M2C_FIELD(temp_r3_2, u8 *, 0x5C), M2C_FIELD(temp_r3_2, u8 *, 0x5D), (s32) M2C_FIELD(temp_r3_2, u8 *, 0x5E), (s32) M2C_FIELD(temp_r3_2, u8 *, 0x5F));
                } else {
                    native_fn_0206006c((0xC * temp_r0_2) + (s32) native_data_ov000_0224621c, (s8) M2C_FIELD(temp_r3_2, u8 *, 0x5C), (s8) M2C_FIELD(temp_r3_2, u8 *, 0x5D), (s8) M2C_FIELD(temp_r3_2, u8 *, 0x5E), (s32) (s8) M2C_FIELD(temp_r3_2, u8 *, 0x5F));
                }
            }
        }
        var_r7 += 1;
    } while ((s32) var_r7 < 0x24);
    if (native_data_ov000_022461f8.field_10 != 0) {
        temp_r0_3 = M2C_FIELD(arg0, s8 *, 0x10);
        if (temp_r0_3 == 2) {
            native_fn_ov000_0221fce0(arg0);
            native_data_ov000_022461f8.field_10 = 0U;
        } else if (temp_r0_3 == 3) {
            native_fn_ov000_022202f4(arg0);
            native_data_ov000_022461f8.field_10 = 0U;
        }
    }
    if ((u32) (u8) (s8) (M2C_FIELD(arg0, s8 *, 0x10) - 1) <= 2U) {
        if (native_data_ov000_022461f8.field_5 != 0) {
            native_fn_ov000_02220be8(arg2, 7);
        } else {
            if (native_data_ov000_022461f8.field_a != 0) {
                native_fn_ov000_02220be8(arg2, 1);
            }
            if (native_data_ov000_022461f8.field_b != 0) {
                native_fn_ov000_02220be8(arg2, 2);
            }
            if (native_data_ov000_022461f8.field_c != 0) {
                native_fn_ov000_02220be8(arg2, 4);
            }
        }
        if (native_data_ov000_022461f8.field_6 != 0) {
            native_fn_ov000_02220ed4(arg2);
        }
        native_data_ov000_022461f8.field_5 = 0U;
        native_data_ov000_022461f8.field_6 = 0U;
        native_data_ov000_022461f8.field_a = 0U;
        native_data_ov000_022461f8.field_b = 0U;
        native_data_ov000_022461f8.field_c = 0U;
    }
    if ((M2C_FIELD(arg0, s8 *, 0x10) == 2) && (native_data_ov000_022461f8.field_1f != 0)) {
        native_fn_ov000_0221cc08();
        native_data_ov000_022461f8.field_1f = 0U;
    }
    if (native_data_ov000_022461f8.field_1 != 0) {
        native_fn_ov000_0221ca80();
        native_data_ov000_022461f8.field_1 = 0U;
    }
    if (sp8 != 0) {
        temp_r0_4 = M2C_FIELD(arg0, s8 *, 0x10);
        switch (temp_r0_4) {
        case 8:
            native_fn_ov000_0221ef90(arg0);
            break;
        case 2:
            native_fn_ov000_0221fce0(arg0);
            native_fn_ov000_02220ed4(arg2);
            break;
        case 3:
            native_fn_ov000_022202f4(arg0);
            native_fn_ov000_02221118(arg2);
            break;
        }
    }
    return native_fn_020851d4();
}
