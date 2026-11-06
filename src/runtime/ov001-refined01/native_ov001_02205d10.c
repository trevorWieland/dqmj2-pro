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
extern u32 native_fn_02048a44();
extern u32 native_fn_0205f98c();
u32 native_ov001_02205d10(void *arg0) {
    u32 temp_r0;
    u8 var_r5;
    u32 var_r6;

    var_r6 = 1;
    var_r5 = 0;
    if ((s32) M2C_FIELD(arg0, s32 *, 0x2C) > 0) {
        do {
            temp_r0 = native_fn_0205f98c(M2C_FIELD(arg0, s32 *, 0x1C), var_r5);
            native_fn_02048a44(temp_r0 + 8, 1);
            var_r5 += 1;
            if (M2C_FIELD(temp_r0, s32 *, 0x14) != 0) {
                var_r6 = 0;
            }
        } while ((s32) var_r5 < (s32) M2C_FIELD(arg0, s32 *, 0x2C));
    }
    return var_r6;
}
