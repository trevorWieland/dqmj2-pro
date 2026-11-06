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
extern u32 native_fn_020080e0();
extern u32 native_fn_0200a2c4();
extern u32 native_fn_0200a3d0();
extern u32 native_fn_0200a41c();
extern u8 native_data_020e3724[];
void native_main_0200808c(void) {
    if (M2C_FIELD(native_data_020e3724, u16 *, 2) != 0) {
        return;
    }
    M2C_FIELD(native_data_020e3724, u16 *, 2) = 1U;
    native_fn_0200a2c4();
    do {

    } while (native_fn_0200a41c(0xC, 1) == 0);
    native_fn_0200a3d0(0xC, native_fn_020080e0);
}
