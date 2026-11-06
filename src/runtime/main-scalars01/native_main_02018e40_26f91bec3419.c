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
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
extern u32 native_fn_02018c94();
extern u32 native_fn_02018cdc();
extern u8 native_data_020ec3a0[];
u32 native_main_02018e40(u32 arg0) {
    u32 temp_r4;

    temp_r4 = native_fn_02007ff4();
    if (native_fn_02018c94() == 0) {
        goto block_2;
    }
    native_fn_02018cdc(*(u32 *)native_data_020ec3a0 + 0xC4, 0, arg0, 0);
block_2:
    return native_fn_02008008(temp_r4);
}
