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
extern u32 native_fn_020bef68();
extern u32 native_fn_020befb8();
extern u32 native_fn_020befc8();
extern u32 native_fn_ov005_021dd590();
extern u32 native_fn_ov005_021e0040();
extern u32 native_fn_ov005_021e0730();
extern u32 native_fn_ov005_021e0818();
extern u32 native_fn_ov005_021e0de0();
extern u32 native_fn_ov005_021e155c();
extern u32 native_fn_ov005_021e63d4();
typedef struct {
    u8 unknown_0[0x1];
    s8 field_1;
    u8 unknown_2[0x3];
    s8 field_5;
    u8 unknown_6[0xe];
    s32 field_14;
    u8 unknown_18[0x8];
    s32 field_20;
    u8 unknown_24[0x20];
    s32 field_44;
} Record_native_data_ov005_021ed438;
extern Record_native_data_ov005_021ed438 native_data_ov005_021ed438;
void native_ov005_021e2444(void) {
    native_fn_020bef68(0);
    native_fn_ov005_021e0818();
    native_fn_ov005_021e0730(0x13, 2, 1);
    native_fn_ov005_021e155c(0xB);
    native_data_ov005_021ed438.field_44 = (s32) native_data_ov005_021ed438.field_14;
    native_fn_ov005_021e63d4();
    native_data_ov005_021ed438.field_5 = 3;
    native_fn_020befb8(1);
    native_fn_020befc8();
    native_fn_ov005_021e0de0(0);
    native_fn_ov005_021e0040();
    native_fn_ov005_021dd590();
    native_data_ov005_021ed438.field_20 = 0;
    native_data_ov005_021ed438.field_1 = 0;
    return;
}
