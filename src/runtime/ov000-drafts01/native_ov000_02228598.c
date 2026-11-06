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
extern u32 native_fn_020449d4();
u32 native_ov000_02228598(s32 arg0) {
    s32 var_r4;
    u32 var_r5;

    var_r5 = 0x2710;
    var_r4 = 0;
    do {
        if ((arg0 == ((u32) (M2C_FIELD((void *) native_fn_020449d4(var_r4), u16 *, 4) << 0x1C) >> 0x1C)) && (((u32) (M2C_FIELD((void *) native_fn_020449d4(var_r4), u16 *, 6) << 0x13) >> 0x13) != 0) && (var_r5 > (u32) ((u32) (M2C_FIELD((void *) native_fn_020449d4(var_r4), u16 *, 6) << 0x13) >> 0x13))) {
            var_r5 = (u32) (M2C_FIELD((void *) native_fn_020449d4(var_r4), u16 *, 6) << 0x13) >> 0x13;
        }
        var_r4 += 1;
    } while (var_r4 < 0x1FF);
    return var_r5;
}
