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
extern u32 native_fn_0200ca84();
extern u32 native_fn_0203d388();
extern u8 native_data_020dd8c8[];
extern u8 native_data_020f6048[];
u32 native_main_0203d3ec(s32 arg0) {
    s32 temp_r5;
    u32 var_r4;

    var_r4 = 1;
    if (M2C_FIELD(native_data_020f6048, u8 *, 0) == 0) {
        goto block_2;
    }
    var_r4 = native_fn_0200ca84(0, M2C_FIELD(native_data_020f6048, s32 *, 8));
    M2C_FIELD(native_data_020f6048, u8 *, 0) = 0;
block_2:
    if (var_r4 == 0) {
        goto block_5;
    }
    if (arg0 == 0xFF) {
        goto block_5;
    }
    goto block_6;
block_5:
    goto block_9;
block_6:
    temp_r5 = *(u32 *)(native_data_020dd8c8 + (arg0 * 4));
    if (native_fn_0203d388(0, temp_r5) != 0) {
        goto block_8;
    }
    var_r4 = 0;
    goto block_9;
block_8:
    M2C_FIELD(native_data_020f6048, u8 *, 0) = 1;
    M2C_FIELD(native_data_020f6048, s32 *, 8) = temp_r5;
block_9:
    return var_r4;
}
