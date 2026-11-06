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
extern u8 native_data_ov001_02238f9c[];
u32 native_ov001_021f1bbc(void) {
    s32 var_r1;
    u8 *var_r2;

    var_r2 = native_data_ov001_02238f9c;
    var_r1 = 0;
loop_1:
    if (*(u32 *)var_r2 != 0x7F) {
        return 1U;
    }
    var_r1 += 1;
    var_r2 += 0x48;
    if (var_r1 >= 0x20) {
        return 0U;
    }
    goto loop_1;
}
