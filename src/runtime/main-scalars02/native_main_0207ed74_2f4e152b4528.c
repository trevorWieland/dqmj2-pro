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
extern u32 native_fn_0202a51c();
extern u32 native_fn_020484dc();
extern u32 native_fn_020485b4();
extern u32 native_fn_0205f920();
extern u8 native_data_021c6c14[];
extern u8 native_data_021c6c30[];
u32 native_main_0207ed74(void) {
    s32 var_r7;

    var_r7 = 0;
loop_1:
    native_fn_0205f920(*(u32 *)(native_data_021c6c30 + (var_r7 * 4)), 1, 2);
    native_fn_0202a51c(*(u32 *)(native_data_021c6c30 + (var_r7 * 4)));
    var_r7 += 1;
    if (var_r7 < 2) {
        goto loop_1;
    }
    if (M2C_FIELD(native_data_021c6c14, s32 *, 0x18) == 0) {
        goto block_4;
    }
    native_fn_020485b4();
block_4:
    return native_fn_020484dc(1, M2C_FIELD(native_data_021c6c14, u8 *, 0));
}
