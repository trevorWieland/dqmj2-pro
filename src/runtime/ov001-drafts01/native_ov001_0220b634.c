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
extern u32 native_fn_020444ec();
extern u32 native_fn_02062850();
extern u32 native_fn_020628b0();
extern u32 native_fn_02062904();
extern u32 native_fn_02062980();
extern u8 native_data_ov001_0223e054[];
u32 native_ov001_0220b634(void) {
    s32 var_r6;
    s32 var_r6_2;
    s32 var_r7;
    u32 temp_r0;
    u32 temp_r0_2;
    u32 var_r4;

    var_r4 = 1;
    if (native_fn_020444ec() == 0) {
        var_r7 = 0;
        do {
            native_fn_020628b0(0);
            native_fn_02062980(0);
            var_r7 += 1;
        } while (var_r7 < 3);
        var_r6 = 0;
        do {
            temp_r0 = native_fn_02062850(M2C_FIELD((native_data_ov001_0223e054 + (var_r6 * 4)), s32 *, 4));
            var_r6 += 1;
            var_r4 &= temp_r0;
        } while (var_r6 < 3);
        var_r6_2 = 0;
        do {
            temp_r0_2 = native_fn_02062904(M2C_FIELD((native_data_ov001_0223e054 + (var_r6_2 * 4)), s32 *, 0x10));
            var_r6_2 += 1;
            var_r4 &= temp_r0_2;
        } while (var_r6_2 < 3);
    }
    return var_r4;
}
