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
extern u32 native_fn_020642dc();
extern u8 native_data_01fff8a0[];
u32 native_main_02067c60(s32 arg0) {
    s32 temp_r0;
    s32 var_r1;
    u8 *var_r2;

    if (native_fn_020642dc() != 0x20) {
        return 1U;
    }
    var_r2 = native_data_01fff8a0;
    var_r1 = 0;
loop_3:
    temp_r0 = *(u32 *)var_r2;
    if ((temp_r0 != 0) && (temp_r0 == arg0)) {
        return 0U;
    }
    var_r1 += 1;
    var_r2 += 0xC;
    if (var_r1 >= 6) {
        return 1U;
    }
    goto loop_3;
}
