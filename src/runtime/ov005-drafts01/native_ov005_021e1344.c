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
extern u32 native_fn_02063520();
extern u32 native_fn_020635d4();
extern u32 native_fn_020bf218();
u32 native_ov005_021e1344(void) {
    s16 temp_r0;
    u32 temp_r5;
    u32 var_r6;
    s32 var_r7;
    void *var_r8;

    var_r6 = 0;
    var_r8 = native_fn_020bf218() + 0xC4;
    var_r7 = 0;
    do {
        temp_r0 = M2C_FIELD(var_r8, s16 *, 0x18);
        if (temp_r0 != 0) {
            temp_r5 = native_fn_02063520(temp_r0, M2C_FIELD(var_r8, u8 *, 0x1A));
            if ((temp_r5 | (native_fn_020635d4(M2C_FIELD(var_r8, s16 *, 0x18), M2C_FIELD(var_r8, u8 *, 0x1A)) * 2)) != 3) {
                var_r6 = 1;
            }
        }
        var_r7 += 1;
        var_r8 += 0x84;
    } while (var_r7 < 3);
    return var_r6;
}
