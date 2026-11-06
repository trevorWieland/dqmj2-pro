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
extern u32 native_fn_02007308();
extern u32 native_fn_0202a37c();
extern u32 native_fn_0202a498();
extern u32 native_fn_0207d9b4();
u32 native_main_0203cc4c(void *arg0, u32 arg1) {
    u32 temp_r0;
    u32 var_r4;
    s32 temp_r5;

    var_r4 = 0;
    if (M2C_FIELD(arg0, s32 *, 0) == 0x485341) {
        temp_r5 = M2C_FIELD(arg0, s32 *, 4);
        if (temp_r5 != 0) {
            temp_r0 = native_fn_0202a37c(arg1, (temp_r5 + 3) & ~3, 4);
            var_r4 = temp_r0;
            if (var_r4 != 0) {
                if (native_fn_0207d9b4(temp_r0, arg0) != 0) {
                    native_fn_02007308(var_r4, temp_r5);
                } else {
                    native_fn_0202a498(arg1, var_r4);
                    var_r4 = 0;
                }
            }
        }
    }
    return var_r4;
}
