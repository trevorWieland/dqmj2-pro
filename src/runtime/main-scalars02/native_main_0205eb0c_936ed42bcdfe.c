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
extern u32 native_fn_0205f2d8();
extern u8 native_data_021079d8[];
u32 native_main_0205eb0c(s32 arg0, s32 arg1, s32 arg2, s32 arg3, s32 arg4) {
    void *temp_r1;

    if (native_fn_0205f2d8() != 0) {
        goto block_2;
    }
    return 0U;
block_2:
    *(u32 *)(native_data_021079d8 + (arg0 * 0x10)) = arg1;
    temp_r1 = native_data_021079d8 + (arg0 * 0x10);
    M2C_FIELD(temp_r1, s32 *, 4) = arg2;
    M2C_FIELD(temp_r1, s32 *, 8) = arg3;
    M2C_FIELD(temp_r1, s32 *, 0xC) = arg4;
    return 1U;
}
