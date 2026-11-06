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
extern u32 native_fn_0202ac08();
extern u32 native_fn_0202ac4c();
extern u32 native_fn_0205d6f4();
extern u32 native_fn_0205d790();
extern u32 native_fn_0207afec();
extern u32 native_fn_ov001_021d7e80();
extern u32 native_fn_ov001_021e9610();
extern u32 native_fn_ov001_021eaa3c();
extern u32 native_fn_ov001_021eaa88();
extern u32 native_fn_ov001_021eea10();
extern u32 native_fn_ov001_021eeb70();
extern u32 native_fn_ov001_021eec7c();
typedef struct {
    u8 unknown_0[0x1];
    s8 field_1;
} Record_native_data_ov001_0222ec84;
extern Record_native_data_ov001_0222ec84 native_data_ov001_0222ec84;
typedef struct {
    u8 unknown_0[0x13];
    s8 field_13;
    u8 unknown_14[0xe];
    u8 field_22;
    u8 unknown_23[0x13];
    u16 field_36;
    u8 unknown_38[0x20];
    u32 field_58;
    u8 unknown_5c[0x4];
    s32 field_60;
} Record_native_data_ov001_02238d7c;
extern Record_native_data_ov001_02238d7c native_data_ov001_02238d7c;
extern u8 native_data_ov001_02238e14[];
u32 native_ov001_021eabac(void) {
    s16 temp_r4;

    if (native_data_ov001_02238d7c.field_22 == 0x0) {
        native_fn_ov001_021d7e80(native_data_ov001_02238d7c.field_60);
        native_fn_ov001_021eaa3c(native_data_ov001_02238d7c.field_36);
        temp_r4 = M2C_FIELD((void *) native_fn_0207afec(native_data_ov001_02238d7c.field_36), s16 *, 0xA);
        native_fn_0202ac08(native_data_ov001_02238e14);
        native_fn_ov001_021eea10(temp_r4, 0);
        native_data_ov001_02238d7c.field_58 = native_fn_ov001_021eec7c(temp_r4, native_data_ov001_02238d7c.field_60, native_fn_0205d790(temp_r4));
        native_data_ov001_02238d7c.field_22 = 0xAU;
    }
    else if (native_data_ov001_02238d7c.field_22 == 0xA) {
        if (native_fn_0205d6f4(native_data_ov001_02238d7c.field_58) == 0) {
            native_data_ov001_02238d7c.field_22 = 0x64U;
        }
    }
    else if (native_data_ov001_02238d7c.field_22 == 0x64) {
        native_fn_ov001_021eeb70(M2C_FIELD((void *) native_fn_0207afec(native_data_ov001_02238d7c.field_36), s16 *, 0xA));
        native_fn_0202ac4c(native_data_ov001_02238e14);
        native_data_ov001_02238d7c.field_22 = 0U;
        native_data_ov001_02238d7c.field_13 = 2;
        native_fn_ov001_021eaa88(native_data_ov001_02238d7c.field_36);
        native_data_ov001_0222ec84.field_1 = (s8) native_fn_ov001_021e9610(0);
    }

    return 0U;
}
