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
extern u32 native_fn_ov001_021db438();
extern u32 native_fn_ov001_021db8d0();
extern u32 native_fn_ov001_021ea428();
u32 native_ov001_021f2408(u32 arg0, u32 arg1, u32 arg2) {
    s32 var_r5;
    u32 temp_r4;
    u32 var_r0;

    if (arg0 == 0) {
        var_r5 = 0;
        do {
            temp_r4 = native_fn_ov001_021db438(arg1, var_r5);
            var_r0 = native_fn_ov001_021db8d0();
            if (var_r0 != 0) {
                var_r0 = native_fn_ov001_021ea428(temp_r4, arg2);
            }
            var_r5 += 1;
        } while (var_r5 < 3);
        return var_r0;
    }
    return native_fn_ov001_021ea428(arg0, arg2);
}
