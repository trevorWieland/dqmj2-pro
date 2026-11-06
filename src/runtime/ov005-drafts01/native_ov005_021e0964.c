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
extern u32 native_fn_0204b61c();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_ov005_021dff78();
extern u32 native_fn_ov005_021e0730();
extern u32 native_fn_ov005_021e08b8();
extern u32 native_fn_ov005_021e0a68();
extern u32 native_fn_ov005_021e0a74();
extern u32 native_fn_ov005_021e0a84();
typedef struct {
    u8 unknown_0[0x28];
    s32 field_28;
} Record_native_data_ov005_021ed234;
extern Record_native_data_ov005_021ed234 native_data_ov005_021ed234;
u32 native_ov005_021e0964(u32 arg0, u32 arg1) {
    native_fn_ov005_021dff78();
    if (M2C_FIELD((void *) native_fn_ov005_021e0a68(), u8 *, 0x11) != 0) {
        return 0U;
    }
    if (!(M2C_FIELD((void *) native_fn_ov005_021e0a84(), u16 *, 2) & 0x800)) {
        return 0U;
    }
    native_fn_0205e7a8(-1, 0x57);
    native_fn_ov005_021e0730(0x13, arg0, arg1);
    native_fn_0204b61c(native_fn_ov005_021e0a74(), 0);
    native_fn_ov005_021e08b8();
    native_data_ov005_021ed234.field_28 = 1;
    return 1U;
}
