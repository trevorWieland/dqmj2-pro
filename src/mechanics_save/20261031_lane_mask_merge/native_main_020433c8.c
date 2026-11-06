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
extern u32 native_fn_02044424(u32 mask);
extern u32 native_fn_02044454(u32 mask);
u32 native_main_020433c8(void *arg0) {
    u32 temp_r0;
    u32 var_r1;
    u8 temp_r2;

    temp_r0 = native_fn_02044424(0);
    temp_r2 = M2C_FIELD(arg0, u8 *, 0x62);
    var_r1 = 0;
    if (temp_r2 & 1) {
        var_r1 |= 2;
    }
    if (temp_r2 & 2) {
        var_r1 |= 0x2000;
    }
    if (temp_r2 & 4) {
        var_r1 |= 0x80;
    }
    if (temp_r2 & 8) {
        var_r1 |= 0x40000000;
    }
    if (temp_r2 & 0x10) {
        var_r1 |= 0x80000000;
    }
    native_fn_02044454(var_r1 | temp_r0);
    return 0U;
}
