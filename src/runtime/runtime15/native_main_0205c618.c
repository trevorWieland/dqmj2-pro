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
extern u32 native_fn_0201d444();
extern u32 native_fn_0202a5c8();
extern u32 native_fn_02040d18();
extern u8 native_data_020ddbbc[];
u32 native_main_0205c618(s32 arg0, u32 arg1) {
    u32 temp_r0;
    u8 sp0[16];

    native_fn_0201d444(&sp0, native_data_020ddbbc, arg1);
    temp_r0 = native_fn_02040d18(arg0, &sp0);
    if (temp_r0 == 0) {
        return 0U;
    }
    return native_fn_0202a5c8(arg0, temp_r0 - arg0);
}
