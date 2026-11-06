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
#define NULL ((void *)0)
extern u32 native_fn_0202a1e0(s32);
extern u32 native_fn_0202a250();
extern void native_fn_02048e74(void *, s32);
extern u32 native_fn_02048fcc(s32);
extern u32 native_fn_0205e73c(u32 arg0);
extern u32 native_fn_0205f5dc();
extern u32 native_fn_02063b40(s32);
extern u32 native_fn_020642dc();
extern u32 native_fn_02068ae8();
extern u32 native_fn_0206c6c0(u32 arg0);
extern u32 native_fn_0207ca14(u32 arg0);
extern u32 native_fn_020bf518(u32);
extern u32 native_fn_020c3a00();
extern u32 native_fn_020c4960();
extern u32 native_fn_020c49e8();
extern u32 native_fn_020c94a8();
extern void native_fn_020cab38(void);
extern u32 native_fn_020cadb0(u32 arg0);
extern u32 native_fn_020cc298();
extern u32 native_fn_020cc2f4();
extern void native_fn_ov000_021f0764(void);
extern u32 native_fn_ov000_021f27d0();
typedef struct { u8 opaque_0[1]; u8 field_1; u8 field_2; u8 field_3; u8 field_4; u8 field_5; u8 opaque_6[10]; u32 field_10; u8 opaque_14[8]; u32 field_1c; u32 field_20; u8 opaque_24[20]; u32 field_38; } ObservedFields_021d6384;
extern ObservedFields_021d6384 native_data_021d6384;
extern u8 native_data_021d63b8[];
typedef struct { u32 field_0; u8 opaque_4[12]; u8 field_10; } ObservedFields_021d63c8;
extern ObservedFields_021d63c8 native_data_021d63c8;

u32 native_main_020c5b00(void) {
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r4;
    u32 var_r0;

    native_data_021d6384.field_1 = 0;
    temp_r0 = native_fn_020642dc() - 8;
    switch (temp_r0) {
    default:
        break;
    case 0:
    case 1:
    case 11:
    case 12:
    case 13:
    case 20:
    case 34:
        native_data_021d6384.field_1 = 1;
        break;
    case 2:
    case 3:
    case 14:
    case 15:
    case 16:
    case 21:
    case 35:
        native_data_021d6384.field_1 = 2;
        break;
    case 24:
        native_data_021d6384.field_1 = 3;
        break;
    }
    temp_r0_2 = native_fn_020c3a00();
    if (temp_r0_2 == 2) {
        native_data_021d6384.field_1 = 1;
    } else if ((u32) (u8) (temp_r0_2 + 0xFD) <= 1U) {
        native_data_021d6384.field_1 = 2;
    }
    native_fn_02048e74(native_data_021d63b8, 1);
    native_fn_02048fcc((s32) (u32) &native_data_021d63c8);
    native_fn_02068ae8();
    var_r0 = native_fn_02063b40(0x13U);
    if (var_r0 == 0) {
        var_r0 = (u32) &native_data_021d6384;
        M2C_FIELD((u32) &native_data_021d6384, s8 *, 6) = 1;
    }
    native_fn_020cadb0(var_r0);
    native_data_021d6384.field_10 = native_fn_0205f5dc();
    native_fn_0205e73c(0x52U);
    native_fn_0205e73c(0x53U);
    native_fn_0205e73c(0x54U);
    native_fn_0205e73c(0x55U);
    native_fn_0205e73c(0x56U);
    native_fn_0205e73c(0x57U);
    temp_r4 = native_fn_0202a1e0(2U);
    native_fn_0207ca14(2U);
    native_fn_0202a1e0((s32) temp_r4);
    native_fn_020bf518(native_fn_0202a250());
    switch (native_data_021d6384.field_1) {
    default:
        break;
    case 0:
        native_data_021d6384.field_5 = 0;
        native_data_021d6384.field_2 = 0;
        native_data_021d6384.field_4 = 0x7F;
        native_data_021d6384.field_3 = 0;
        native_fn_ov000_021f0764();
        native_fn_ov000_021f27d0();
        native_data_021d63c8.field_10 = 0;
        break;
    case 1:
        native_data_021d6384.field_5 = 0;
        native_data_021d6384.field_2 = 1;
        native_data_021d6384.field_4 = 0x7F;
        native_data_021d6384.field_3 = 1;
        native_data_021d63c8.field_10 = 1;
        break;
    case 2:
        native_fn_020cab38();
        native_fn_020c94a8();
        native_fn_020c49e8();
        native_fn_020c4960();
        native_data_021d6384.field_4 = 0x7F;
        native_data_021d6384.field_3 = 0xA;
        native_data_021d6384.field_2 = 0xA;
        native_data_021d63c8.field_10 = 0xA;
        native_data_021d6384.field_5 = 0xA;
        native_data_021d6384.field_38 = 1;
        native_fn_020cc298();
        native_fn_020cc2f4();
        break;
    case 3:
        native_data_021d6384.field_5 = 0;
        native_data_021d6384.field_2 = 2;
        native_data_021d6384.field_4 = 0x7F;
        native_data_021d6384.field_3 = 2;
        native_data_021d63c8.field_10 = 2;
        break;
    }
    native_data_021d63c8.field_0 = 0;
    native_fn_0206c6c0(2U);
    native_data_021d6384.field_20 = 0;
    native_data_021d6384.field_1c = 0;
    return (u32) &native_data_021d6384;
}
