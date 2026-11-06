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
extern u32 native_fn_02067818();
extern u32 native_fn_020679f0();
u32 native_ov006_021e3b10(void) {
    u32 temp_r0;
    u32 var_r0;
    u32 temp_r4;
    s32 var_r5;
    u32 temp_r6;

    temp_r6 = native_fn_02067818();
    var_r5 = 0;
loop_1:
    temp_r4 = M2C_FIELD(temp_r6, s32 *, 4) + var_r5;
    if (temp_r4 == M2C_FIELD((void *) native_fn_020679f0(), s32 *, 4)) {
        temp_r0 = M2C_FIELD(((var_r5 * 0x24) + temp_r6), u32 *, 0x10);
        if (temp_r0 == 0) {
            return 0U;
        }
        if (temp_r4 < temp_r0) {
            return 0U;
        }
        if (temp_r4 > temp_r0) {
            var_r0 = 1;
        } else {
            var_r0 = 2;
        }
        return var_r0;
    }
    var_r5 += 1;
    if (var_r5 >= 0xA) {
        return -1U;
    }
    goto loop_1;
}
