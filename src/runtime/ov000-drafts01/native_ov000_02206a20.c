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
extern u32 native_fn_02049ad0();
extern u32 native_fn_02049ffc();
extern u32 native_fn_0204a104();
u32 native_ov000_02206a20(u32 arg0, u32 arg1, u32 arg2, s32 arg3) {
    s32 temp_r0;

    temp_r0 = M2C_FIELD(*(void **) native_fn_02049ad0(), s32 *, 4);
    if (arg3 != 0) {
        native_fn_02049ffc(temp_r0);
    }
    return native_fn_0204a104(arg0, arg2, 1, arg1);
}
