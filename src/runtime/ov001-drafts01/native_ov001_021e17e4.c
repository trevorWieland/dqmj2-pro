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
extern u32 native_fn_02044cdc();
extern u32 native_fn_ov001_02210ad0();
u32 native_ov001_021e17e4(u32 arg0, void *arg1) {
    u32 temp_r0;
    u32 var_r0;
    u32 var_r0_2;

    temp_r0 = native_fn_02044cdc(M2C_FIELD(M2C_FIELD(arg1, void **, 0x1E8), s16 *, 0x2A));
    switch (temp_r0) {
    case 0:
        return 1U;
    case 1:
        if (native_fn_ov001_02210ad0(arg0, 2, 1) != 0) {
            var_r0 = 1;
        } else {
            var_r0 = 0;
        }
        return var_r0;
    case 2:
        if (native_fn_ov001_02210ad0(arg0, 4, 1) != 0) {
            var_r0_2 = 1;
        } else {
            var_r0_2 = 0;
        }
        return var_r0_2;
    default:
        return 0U;
    }
}
