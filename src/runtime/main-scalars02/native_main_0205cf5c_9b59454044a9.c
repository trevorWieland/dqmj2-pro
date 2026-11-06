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
extern u32 native_fn_02008c14();
extern u32 native_fn_02028dac();
extern u32 native_fn_020297e0();
extern u32 native_fn_02029950();
extern u32 native_fn_0204124c();
extern u8 native_data_02102e38[];
u32 native_main_0205cf5c(void *arg0) {
    s32 temp_r4;

    temp_r4 = *(u32 *)(native_data_02102e38 + (M2C_FIELD(arg0, s8 *, 1) * 0xAC));
    if (!(temp_r4 & 2)) {
        goto block_2;
    }
    native_fn_0204124c(arg0 + 0x14);
block_2:
    if (!(temp_r4 & 4)) {
        goto block_4;
    }
    native_fn_020297e0(arg0 + 0x14);
block_4:
    if (!(temp_r4 & 8)) {
        goto block_6;
    }
    native_fn_02029950(arg0 + 0x14);
block_6:
    if (!(temp_r4 & 1)) {
        goto block_8;
    }
    native_fn_02028dac(arg0 + 0x14);
block_8:
    native_fn_02008c14(0, arg0, 0x11C);
    return 1U;
}
