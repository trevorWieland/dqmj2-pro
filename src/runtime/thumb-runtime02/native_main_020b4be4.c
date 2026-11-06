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
extern u32 native_fn_020a8640();
extern u32 native_fn_020a8644();
extern u32 native_fn_020a8720();
extern u32 native_fn_020b3bb8();
u32 native_main_020b4be4(void *arg0, void *arg1, u32 arg2) {
    s32 sp4;
    u32 sp0;
    s32 temp_r0_3;
    s32 temp_r1;
    s32 temp_r2;
    s32 temp_r7;
    s32 var_r4;
    s32 var_r5;
    u32 temp_r0;
    void *temp_r0_2;

    temp_r7 = M2C_FIELD(arg1, s32 *, 4);
    sp4 = M2C_FIELD(arg1, s32 *, 0);
    var_r5 = 0;
    native_fn_020a8720(M2C_FIELD(arg0, s32 *, 0x5C), arg2);
    temp_r0 = native_fn_020a8640(M2C_FIELD(arg0, s32 *, 0x5C));
    var_r4 = 0;
    sp0 = temp_r0;
    if ((s32) temp_r0 > 0) {
        do {
            temp_r0_2 = (void *) native_fn_020a8644(M2C_FIELD(arg0, s32 *, 0x5C), var_r4);
            temp_r2 = M2C_FIELD(temp_r0_2, s32 *, 0);
            if (temp_r2 > sp4) {
                temp_r1 = temp_r2 - temp_r7;
                M2C_FIELD(temp_r0_2, s32 *, 0) = temp_r1;
                temp_r0_3 = temp_r1 + M2C_FIELD(temp_r0_2, s32 *, 4);
                if (var_r5 <= temp_r0_3) {
                    var_r5 = temp_r0_3;
                }
            }
            var_r4 += 1;
        } while (var_r4 < (s32) sp0);
    }
    return native_fn_020b3bb8(arg0 + 0x44, sp4, temp_r7);
}
