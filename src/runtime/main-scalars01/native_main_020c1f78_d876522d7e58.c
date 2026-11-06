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
extern u8 native_data_021d4c28[];
u32 native_main_020c1f78(u32 arg0) {
    u32 var_r0;

    var_r0 = arg0;
    if (*(u32 *)native_data_021d4c28 != 0) {
        goto block_2;
    }
    return 0U;
block_2:
    if (var_r0 < 3U) {
        goto block_4;
    }
    var_r0 = 0;
block_4:
    return (0xC * var_r0) + *(u32 *)native_data_021d4c28;
}
