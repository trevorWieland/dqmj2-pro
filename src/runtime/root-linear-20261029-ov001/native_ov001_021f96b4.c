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
extern u32 native_fn_0205c904();
extern u32 native_fn_0205f5dc();
extern u32 native_fn_0205fd60();
extern u32 native_fn_ov001_021d732c();
extern u32 native_fn_ov001_021d7564();
extern u32 native_fn_ov001_021e35b4();
extern u32 native_fn_ov001_021eea10();
extern u32 native_fn_ov001_021f9418();
extern u8 native_data_ov001_0222ed2c[];
typedef struct {
    u8 unknown_0[0x7];
    u8 field_7;
    u8 unknown_8[0x2];
    s8 field_a;
    u8 unknown_b[0x31];
    u32 field_3c;
} Record_native_data_ov001_02239a14;
extern Record_native_data_ov001_02239a14 native_data_ov001_02239a14;
u32 native_ov001_021f96b4(void) {
    if (native_data_ov001_02239a14.field_7 == 0x0) {
        native_fn_ov001_021d732c(0x2C, 2);
        native_fn_ov001_021d7564(0x2C, native_data_ov001_0222ed2c, 0);
        native_data_ov001_02239a14.field_7 = 5U;
    }
    else if (native_data_ov001_02239a14.field_7 == 0x5) {
        if (native_fn_0205fd60() == 0) {
            native_data_ov001_02239a14.field_7 = 0xAU;
        }
    }
    else if (native_data_ov001_02239a14.field_7 == 0xA) {
        native_fn_ov001_021eea10(8, 0);
        native_data_ov001_02239a14.field_7 = 0x14U;
    }
    else if (native_data_ov001_02239a14.field_7 == 0x14) {
        native_fn_0205c904(8);
        native_fn_ov001_021eea10(0x3C, 0);
        native_data_ov001_02239a14.field_7 = 0x1EU;
    }
    else if (native_data_ov001_02239a14.field_7 == 0x1E) {
        native_fn_0205c904(0x3C);
        native_fn_ov001_021eea10(0x3D, 0);
        native_data_ov001_02239a14.field_7 = 0x28U;
    }
    else if (native_data_ov001_02239a14.field_7 == 0x28) {
        native_fn_0205c904(0x3D);
        native_fn_ov001_021eea10(0x3E, 0);
        native_data_ov001_02239a14.field_7 = 0x32U;
    }
    else if (native_data_ov001_02239a14.field_7 == 0x32) {
        native_fn_0205c904(0x3E);
        native_fn_ov001_021eea10(0x3F, 0);
        native_data_ov001_02239a14.field_7 = 0x3CU;
    }
    else if (native_data_ov001_02239a14.field_7 == 0x3C) {
        native_fn_0205c904(0x3F);
        native_data_ov001_02239a14.field_7 = 0x46U;
    }
    else if (native_data_ov001_02239a14.field_7 == 0x46) {
        native_data_ov001_02239a14.field_3c = native_fn_0205f5dc();
        native_fn_ov001_021f9418();
        native_data_ov001_02239a14.field_7 = 0x50U;
    }
    else if (native_data_ov001_02239a14.field_7 == 0x50) {
        native_fn_ov001_021e35b4(0x16);
        native_data_ov001_02239a14.field_7 = 0x5AU;
    }
    else if (native_data_ov001_02239a14.field_7 == 0x5A) {
        native_fn_ov001_021e35b4(0x17);
        native_data_ov001_02239a14.field_7 = 0x64U;
    }
    else if (native_data_ov001_02239a14.field_7 == 0x64) {
        native_data_ov001_02239a14.field_a = 2;
        native_data_ov001_02239a14.field_7 = 0U;
    }

    return 0U;
}
