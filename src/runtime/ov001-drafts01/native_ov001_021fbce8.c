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
extern u32 native_fn_0205f5f4();
extern u32 native_fn_ov001_021d7584();
extern u32 native_fn_ov001_021e36a4();
extern u32 native_fn_ov001_021eeb70();
typedef struct {
    u8 unknown_0[0xa];
    s8 field_a;
    u8 unknown_b[0x31];
    s32 field_3c;
} Record_native_data_ov001_02239a14;
extern Record_native_data_ov001_02239a14 native_data_ov001_02239a14;
u32 native_ov001_021fbce8(void) {
    native_fn_ov001_021e36a4(0x17);
    native_fn_ov001_021e36a4(0x16);
    native_fn_ov001_021eeb70(0x3F);
    native_fn_ov001_021eeb70(0x3E);
    native_fn_ov001_021eeb70(0x3D);
    native_fn_ov001_021eeb70(0x3C);
    native_fn_ov001_021eeb70(8);
    native_fn_ov001_021d7584(0x2C);
    native_fn_0205f5f4(native_data_ov001_02239a14.field_3c);
    native_data_ov001_02239a14.field_a = 0x10;
    return 1U;
}
