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
extern u32 native_fn_02068c14();
extern u32 native_fn_02068eb8();
extern u32 native_fn_ov001_0220267c();
extern u32 native_fn_ov001_02203554();
extern u32 native_fn_ov001_0220364c();
extern u32 native_fn_ov001_0220375c();
extern u32 native_fn_ov001_02203f28();
typedef struct {
    u8 unknown_0[0x8];
    s8 field_8;
} Record_native_data_ov001_0223d8ec;
extern Record_native_data_ov001_0223d8ec native_data_ov001_0223d8ec;
u32 native_ov001_022037b4(void) {
    native_fn_ov001_0220364c();
    native_fn_ov001_0220375c();
    native_fn_ov001_02203554();
    native_fn_ov001_02203f28();
    native_fn_02068eb8(0, 0, 0, -1);
    native_fn_02068c14(5, 0x6F, 0x6B, 0);
    native_fn_ov001_0220267c();
    native_data_ov001_0223d8ec.field_8 = 2;
    return 0U;
}
