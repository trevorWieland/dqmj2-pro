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
extern u32 native_fn_020136fc();
extern u32 native_fn_020824c4();
extern u8 native_data_021c74c0[];
extern u8 native_data_021c7ee0[];
u32 native_main_02083b40(u32 arg0) {
    u32 temp_r0;

    temp_r0 = native_fn_020136fc(native_data_021c7ee0, arg0, native_data_021c74c0);
    if (temp_r0 != 7) {
        goto block_2;
    }
    return 1U;
block_2:
    if (temp_r0 != 5) {
        goto block_4;
    }
    native_fn_020824c4();
    return 0U;
block_4:
    if (temp_r0 != 0) {
        goto block_6;
    }
    return 1U;
block_6:
    native_fn_020824c4();
    return 0U;
}
