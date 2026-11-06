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
extern u32 native_fn_0207b674();
extern u32 native_fn_ov001_021db8d0();
extern u8 native_data_ov001_0222e118[];
u32 native_ov001_02221720(void *arg0) {
    s32 var_r6;
    s32 var_r7;
    void *var_r8;
    u8 *var_r9;

    var_r6 = 0;
    var_r8 = M2C_FIELD(arg0, void **, 8);
loop_1:
    var_r7 = 0;
    var_r9 = native_data_ov001_0222e118;
loop_2:
    if ((native_fn_ov001_021db8d0(var_r8) != 0) && (M2C_FIELD(var_r8, s8 *, 0x261) == 0) && ((s32) native_fn_0207b674(*var_r9, M2C_FIELD(var_r8, s32 *, 0x1E8) + 0x46) > 0)) {
        return 0U;
    }
    var_r7 += 1;
    var_r9 += 1;
    if (var_r7 >= 0x1D) {
        var_r6 += 1;
        var_r8 += 0x440;
        if (var_r6 >= 3) {
            return 1U;
        }
        goto loop_1;
    }
    goto loop_2;
}
