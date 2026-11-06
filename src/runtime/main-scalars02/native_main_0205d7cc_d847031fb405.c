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
extern u32 native_fn_0205ca0c();
extern u8 native_data_02102ea4[];
u32 native_main_0205d7cc(void) {
    s32 temp_r0;
    u16 var_r4;

    var_r4 = 0;
    temp_r0 = (s32) native_fn_0205ca0c();
    if (temp_r0 < 0) {
        goto block_2;
    }
    var_r4 = *(u16 *)(native_data_02102ea4 + (temp_r0 * 0xAC));
block_2:
    return (u32) var_r4;
}
