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
extern u32 native_fn_02008e0c();
extern u32 native_fn_020824b4();
extern u32 native_fn_02082ee4();
extern u32 native_fn_02082f7c();
extern u8 native_data_021c72a0[] __attribute__((aligned(2)));
extern u8 native_data_021c7400[];
u32 native_main_02083a90(s32 arg0, u32 arg1) {
    M2C_FIELD(native_data_021c72a0, s32 *, 0x54) = (s32) (((M2C_FIELD(native_data_021c72a0, u16 *, 0x12) + 0x55) & ~0x1F) * 2);
    M2C_FIELD(native_data_021c72a0, s32 *, 0x58) = (s32) ((M2C_FIELD(native_data_021c72a0, u16 *, 0x16) + 0x21) & ~0x1F);
    M2C_FIELD(native_data_021c72a0, s32 *, 0x50) = arg0;
    native_fn_020824b4(3);
    if (arg0 == 1) {
        goto block_4;
    }
    if (arg0 == 3) {
        goto block_4;
    }
    if (arg0 == 5) {
        goto block_4;
    }
    goto block_7;
block_4:
    native_fn_02008e0c(arg1, native_data_021c7400, 0xC0);
    if (M2C_FIELD(native_data_021c72a0, s32 *, 0x40) == 0) {
        goto block_6;
    }
    return native_fn_02082ee4();
block_6:
    return native_fn_02082f7c();
block_7:
    return 0U;
}
