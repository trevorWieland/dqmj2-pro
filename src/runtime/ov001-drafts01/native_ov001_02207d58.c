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
extern u32 native_fn_020456ac();
extern u32 native_fn_ov001_02207938();
u32 native_ov001_02207d58(void) {
    s8 var_r0;
    u32 var_r4;

    var_r4 = native_fn_ov001_02207938();
    native_fn_020456ac(1, 2, 1, 0xB, 0x1E, 0xC);
    var_r0 = 0;
    do {
        var_r0 += 1;
        M2C_FIELD(var_r4, s16 *, 0x70) = 0;
        var_r4 += 0x46;
    } while ((s32) var_r0 < 2);
    return (u32) var_r0;
}
