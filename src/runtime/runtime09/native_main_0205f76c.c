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
extern u32 native_fn_020381b4();
extern u8 native_data_021b8ae0[];
extern u8 native_data_021b8b10[];
u32 native_main_0205f76c(u32 arg0, u32 arg1) {
    u32 var_r3;
    void *temp_r0;

    var_r3 = 0;
    if (arg0 >= 0x10U) {
        goto block_4;
    }
    temp_r0 = native_data_021b8b10 + (arg0 * 8);
    if ((s32) M2C_FIELD(temp_r0, s16 *, 4) < 0) {
        goto block_3;
    }
    native_fn_020381b4(temp_r0, 0xFFFF, arg1);
    M2C_FIELD(native_data_021b8ae0, s8 *, 1) = 0;
    var_r3 = 1;
    goto block_5;
block_3:
    M2C_FIELD(native_data_021b8ae0, s8 *, 1) = 8;
    goto block_5;
block_4:
    M2C_FIELD(native_data_021b8ae0, s8 *, 1) = 0xC;
block_5:
    return var_r3;
}
