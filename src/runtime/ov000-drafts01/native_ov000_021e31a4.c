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
extern u32 native_fn_0205cedc();
extern u32 native_fn_0205cf14();
extern u32 native_fn_ov000_021e31f0();
extern u32 native_fn_ov000_021e3370();
extern u8 native_data_ov000_022322d0[];
u32 native_ov000_021e31a4(void) {
    s8 temp_r5;
    u32 temp_r0;
    u32 temp_r4;

    temp_r5 = M2C_FIELD(native_data_ov000_022322d0, s8 *, 2);
    if ((s32) temp_r5 < 0) {
        return (u32) native_data_ov000_022322d0;
    }
    temp_r4 = native_fn_0205cedc(temp_r5);
    temp_r0 = native_fn_0205cf14(temp_r5);
    if (temp_r4 != temp_r0) {
        return temp_r0;
    }
    native_fn_ov000_021e3370(2);
    return native_fn_ov000_021e31f0(0xD, 0);
}
