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
extern u32 native_fn_02026144();
extern u32 native_fn_0207b244();
extern u32 native_fn_ov001_021db8d0();
extern u32 native_fn_ov001_021dbd24();
extern u32 native_fn_ov001_021dbd30();
extern u32 native_fn_ov001_02218c34();
u32 native_ov001_0221ee44(void *arg0) {
    s32 temp_r0;
    u32 temp_r5;
    u32 var_r5;
    void *temp_r6;
    s32 temp_r7;
    s32 var_r8;
    s32 var_r9;

    temp_r6 = M2C_FIELD(arg0, void **, 0);
    temp_r7 = M2C_FIELD(arg0, s32 *, 0xC);
    var_r9 = M2C_FIELD(arg0, s32 *, 8);
    var_r8 = 0;
loop_1:
    if (native_fn_ov001_021db8d0(var_r9) != 0) {
        temp_r5 = native_fn_ov001_021dbd24(var_r9);
        if ((s32) temp_r5 <= (s32) native_fn_ov001_02218c34(temp_r6, var_r9, temp_r7)) {
            var_r5 = native_fn_0207b244(temp_r7, native_fn_ov001_021dbd30(temp_r6), M2C_FIELD(temp_r6, s32 *, 0x1E8) + 0x46);
            if (var_r5 == 0) {
                var_r5 = 1;
            }
            temp_r0 = (native_fn_02026144(0x32, var_r5) - (var_r5 * 2)) + 0x32;
            M2C_FIELD(arg0, s32 *, 0x18) = temp_r0;
            if (temp_r0 < 0) {
                M2C_FIELD(arg0, s32 *, 0x18) = 0;
            }
            return 1U;
        }
    }
    var_r8 += 1;
    var_r9 += 0x440;
    if (var_r8 >= 3) {
        return 0U;
    }
    goto loop_1;
}
