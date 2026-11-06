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
extern u32 native_fn_020456ac();
extern u32 native_fn_02063dc8();
extern u32 native_fn_02063e38();
u32 native_main_0204b79c(void) {
    s8 temp_r0_3;
    void *temp_r0;
    void *temp_r0_2;
    u8 temp_r2;
    s8 var_r8;
    s32 temp_gt;

    temp_r0 = (void *) native_fn_02063e38();
    var_r8 = 0;
    if ((s32) M2C_FIELD(temp_r0, s16 *, 0x64) > 0) {
        do {
            temp_r0_2 = temp_r0 + var_r8;
            temp_r2 = M2C_FIELD(temp_r0_2, u8 *, 0x68);
            if (temp_r2 != -1U) {
                native_fn_020456ac(1, 2, temp_r2, M2C_FIELD(temp_r0_2, u8 *, 0x70), 3, 3);
            }
            temp_r0_3 = var_r8 + 1;
            temp_gt = (s32) M2C_FIELD(temp_r0, s16 *, 0x64) > (s32) temp_r0_3;
            var_r8 = temp_r0_3;
        } while (temp_gt);
    }
    return native_fn_02063dc8();
}
