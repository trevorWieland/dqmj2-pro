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
extern u32 native_fn_02044dc4();
extern u8 native_data_021c4c02[];
extern u8 native_data_021c4c04[];
u32 native_main_0206da90(s32 arg0) {
    s32 temp_r2;

    temp_r2 = arg0 * 0x18;
    if (native_fn_02044dc4(*(s16 *)(native_data_021c4c02 + temp_r2), *(native_data_021c4c04 + temp_r2)) < 7U) {
        goto block_2;
    }
    return 1U;
block_2:
    return 0U;
}
