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
extern u32 native_fn_02010ba8();
extern u8 native_data_020dce80[];
u32 native_main_02010fa8(void) {
    native_fn_02010ba8(0xB8000000, 0);
    *(s32 *)0x040001A4 = ((M2C_FIELD(*(u32 *)native_data_020dce80, s32 *, 0x60) & ~0x07000000) | 0xA7000000) & ~0x1FFF;
loop_1:
    if (!(*(s32 *)0x040001A4 & 0x800000)) {
        goto loop_1;
    }
    return *(u32 *)0x04100010;
}
