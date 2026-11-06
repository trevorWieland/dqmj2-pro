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
extern u32 native_fn_0203917c();
extern u32 native_fn_0203b3f8();
extern u32 native_fn_0203b46c();
extern u32 native_fn_0203b47c();
extern u32 native_fn_0203b4b4();
extern u32 native_fn_0203b4c4();
extern u32 native_fn_0203b4ec();
extern u32 native_fn_0203b4f0();
extern u32 native_fn_0203b50c();
u32 native_main_0203b378(void *arg0, u32 arg1) {
    if (native_fn_0203917c(arg1) == 0) {
        M2C_FIELD(arg0, u32 (**)(), 0x164) = native_fn_0203b3f8;
        M2C_FIELD(arg0, u32 (**)(), 0x168) = native_fn_0203b46c;
        M2C_FIELD(arg0, u32 (**)(), 0x16C) = native_fn_0203b47c;
        M2C_FIELD(arg0, u32 (**)(), 0x170) = native_fn_0203b4b4;
        return (u32) native_fn_0203b4b4;
    }
    M2C_FIELD(arg0, u32 (**)(), 0x164) = native_fn_0203b4c4;
    M2C_FIELD(arg0, u32 (**)(), 0x168) = native_fn_0203b4ec;
    M2C_FIELD(arg0, u32 (**)(), 0x16C) = native_fn_0203b4f0;
    M2C_FIELD(arg0, u32 (**)(), 0x170) = native_fn_0203b50c;
    return (u32) native_fn_0203b50c;
}
