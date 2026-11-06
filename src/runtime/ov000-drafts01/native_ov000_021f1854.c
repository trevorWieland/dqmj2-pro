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
extern u32 native_fn_02062b9c();
extern u32 native_fn_02062bf0();
extern u32 native_fn_02062c44();
extern u32 native_fn_020c1f78();
u32 native_ov000_021f1854(u32 arg0, u32 arg1) {
    s32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r4;

    temp_r0 = (s32) native_fn_02062b9c();
    if (temp_r0 > 0) {
        temp_r4 = native_fn_02062bf0(arg0, arg1);
        temp_r0_2 = native_fn_02062c44(arg0, arg1);
        if (temp_r0 > (s32) (temp_r4 + temp_r0_2)) {
            return native_fn_020c1f78(2);
        }
        if ((s32) temp_r0_2 > 0) {
            return native_fn_020c1f78(1);
        }
        return native_fn_020c1f78(0);
    }
    return 0U;
}
