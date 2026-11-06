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
extern u32 native_fn_0202a1e0(u32);
extern u32 native_fn_02041538(u32, u32, u32);
extern u32 native_fn_02041814(void);
extern u32 native_fn_02048f5c(u32);
extern u32 native_fn_02048f6c(u32);
extern u32 native_fn_02068ae8(void);
extern u32 native_fn_020c42c8(void);
extern u32 native_fn_020c4928(u32, u32);
extern u32 native_fn_020c7044(void);
extern u32 native_fn_020c70cc(void);
extern u32 native_fn_020cc704(void);
extern u32 native_fn_020cc724(void);
extern u32 native_fn_ov000_021f0624(void);
extern u32 native_fn_ov000_021f0874(void);
extern u32 native_fn_ov000_021f2a20(u32, u32);
extern u32 native_fn_ov000_021f2c38(u32);
extern u32 native_fn_ov000_021f31a4(void);
extern u32 native_fn_ov000_021f33a0(void);
typedef struct {
    u8 unknown_0[0x1];
    u8 field_1;
    u8 unknown_2[0x1];
    s8 field_3;
    u8 unknown_4[0x8];
    s32 field_c;
    u8 unknown_10[0x4];
    s32 field_14;
} Record_native_data_021d6384;
extern Record_native_data_021d6384 native_data_021d6384;
typedef struct {
    u8 unknown_0[0x10];
    s8 field_10;
} Record_native_data_021d63c8;
extern Record_native_data_021d63c8 native_data_021d63c8;
u32 native_main_020c7ee8(void) {
    u32 temp_r4;

    switch (native_data_021d63c8.field_10) {
    case 9: goto block_3;
    case 10: goto block_9;
    default: goto block_16;
    }
block_3:
    if (native_data_021d6384.field_c != 0) {
        goto block_6;
    }
    if (native_fn_ov000_021f0874() == 0) {
        goto block_16;
    }
    native_fn_02041538(1, 2, 0xA);
    native_data_021d6384.field_c = 0xA;
    goto block_16;
block_6:
    if (native_data_021d6384.field_c != 0xA) {
        goto block_16;
    }
    native_fn_ov000_021f2a20(native_fn_ov000_021f0624(), 3);
    if (native_fn_02041814() == 1) {
        goto block_16;
    }
    native_fn_ov000_021f31a4();
    native_fn_ov000_021f33a0();
    native_fn_ov000_021f2c38(0);
    native_fn_020c4928(native_fn_02048f6c(1), 0x20);
    native_fn_020c4928(native_fn_02048f5c(1), 0x20);
    native_fn_020c7044();
    native_data_021d6384.field_3 = (s8) native_data_021d63c8.field_10;
    native_data_021d63c8.field_10 = 0;
    native_data_021d6384.field_14 = 1;
    native_data_021d6384.field_c = 0;
    return 1U;
block_9:
    if (native_data_021d6384.field_c != 0) {
        goto block_12;
    }
    if (native_fn_020cc704() == 0) {
        goto block_16;
    }
    native_data_021d6384.field_c = 1;
    goto block_16;
block_12:
    if (native_data_021d6384.field_c != 1) {
        goto block_16;
    }
    native_fn_020cc724();
    if (native_data_021d6384.field_1 != 2) {
        goto block_15;
    }
    native_data_021d6384.field_c = 0;
    return 1U;
block_15:
    temp_r4 = native_fn_0202a1e0(2U);
    native_fn_02068ae8();
    native_fn_020c70cc();
    native_fn_020c42c8();
    native_fn_0202a1e0(temp_r4);
    native_data_021d6384.field_3 = (s8) native_data_021d63c8.field_10;
    native_data_021d63c8.field_10 = 0;
    native_data_021d6384.field_14 = 1;
    native_data_021d6384.field_c = 0;
    return 1U;
block_16:
    return 0U;
}
