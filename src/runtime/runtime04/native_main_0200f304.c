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
extern u32 native_fn_0200a2c4();
extern u32 native_fn_0200a3d0();
extern u32 native_fn_0200a41c();
extern u32 native_fn_0200f578();
extern u8 native_data_020e5438[];
void native_main_0200f304(void) {
    if (M2C_FIELD(native_data_020e5438, u16 *, 0) != 0) {
        return;
    }
    M2C_FIELD(native_data_020e5438, u16 *, 0) = 1U;
    M2C_FIELD(native_data_020e5438, s32 *, 0xC) = 0;
    M2C_FIELD(native_data_020e5438, s32 *, 0x10) = 0;
    M2C_FIELD(native_data_020e5438, s32 *, 0x28) = 0;
    M2C_FIELD(native_data_020e5438, s32 *, 0x14) = 0;
    M2C_FIELD(native_data_020e5438, s32 *, 0x18) = 0;
    native_fn_0200a2c4();
    do {

    } while (native_fn_0200a41c(5, 1) == 0);
    native_fn_0200a3d0(5, native_fn_0200f578);
}
