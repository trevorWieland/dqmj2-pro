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
extern u8 native_data_021d71ec[];
u32 native_main_020d3564(s32 arg0) {
    u8 var_r2;

    var_r2 = 0;
    if (*(u32 *)native_data_021d71ec == 0) {
        goto block_2;
    }
    var_r2 = M2C_FIELD((*(u32 *)native_data_021d71ec + (arg0 * 4)), u8 *, 8);
block_2:
    return (u32) var_r2;
}
