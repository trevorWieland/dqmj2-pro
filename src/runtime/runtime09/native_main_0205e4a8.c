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
extern u32 native_fn_02038008();
extern u32 native_fn_0205e520();
extern u32 native_fn_0205ed74();
extern u32 native_fn_0205f5dc();
extern u8 native_data_020ddc94[];
extern u8 native_data_021079a0[];
extern u8 native_data_02107ae0[];
u32 native_main_0205e4a8(void) {
    s32 var_r5;
    u32 var_r4;

    var_r4 = 0;
    if (native_fn_0205ed74(native_data_02107ae0, 0xB1000, native_data_020ddc94, 0xA) == 0) {
        goto block_5;
    }
    var_r5 = 0;
    goto loop_3;
block_2:
    native_fn_02038008(var_r5, 4);
    var_r5 += 1;
loop_3:
    if (var_r5 < 0x20) {
        goto block_2;
    }
    M2C_FIELD(native_data_021079a0, u32 *, 4) = native_fn_0205f5dc();
    M2C_FIELD(native_data_021079a0, s32 *, 0x10) = 0;
    var_r4 = native_fn_0205e520();
block_5:
    return var_r4;
}
