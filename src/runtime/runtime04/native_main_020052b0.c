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
extern u32 native_fn_02003b40();
extern u8 native_data_020e3320[];
void native_main_020052b0(void) {
    u32 temp_r0;

    temp_r0 = native_fn_02003b40();
    M2C_FIELD(native_data_020e3320, u32 *, 8) = temp_r0;
    switch (temp_r0) {
    case 0x0:
        return;
    case 0x40:
        M2C_FIELD(native_data_020e3320, s32 *, 4) = 0x06894000;
        return;
    case 0x20:
        M2C_FIELD(native_data_020e3320, s32 *, 4) = 0x06890000;
        return;
    }
}
