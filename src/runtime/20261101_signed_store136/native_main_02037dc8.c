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
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
#define NULL ((void *)0)
extern u32 native_fn_020094b4();
extern u32 native_fn_0200f218();
extern u32 native_fn_0200f230();
extern u32 native_fn_02037750();
extern void native_fn_02037fac();
extern u32 native_fn_02037fe4();
extern u32 native_fn_02038248();
extern void native_fn_020389d8();
extern u8 native_data_020f1f64[];
extern u8 native_data_020f1f74[];
extern u8 native_data_020f1f80[];
u32 native_main_02037dc8(void) {
    if (M2C_FIELD(native_data_020f1f64, s32 *, 0xC) != 0) {
        return (u32) native_data_020f1f64;
    }
    M2C_FIELD(native_data_020f1f64, s32 *, 0xC) = 1;
    native_fn_020094b4();
    M2C_FIELD(native_data_020f1f64, void (**)(), 0x10) = native_fn_02037fac;
    M2C_FIELD(native_data_020f1f64, s32 *, 0x14) = 0;
    M2C_FIELD(native_data_020f1f64, u32 (**)(), 0x1C) = native_fn_02037fe4;
    M2C_FIELD(native_data_020f1f64, s32 *, 0x20) = 0;
    native_fn_0200f218((u32) native_data_020f1f74);
    native_fn_0200f230((u32) native_data_020f1f80);
    native_fn_020389d8();
    native_fn_02037750();
    native_fn_02038248();
    M2C_FIELD(native_data_020f1f64, s8 *, 0) = -1U;
    M2C_FIELD(native_data_020f1f64, s32 *, 4) = 1;
    return (u32) native_data_020f1f64;
}
