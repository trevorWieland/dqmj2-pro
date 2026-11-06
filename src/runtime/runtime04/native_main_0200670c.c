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
extern u32 native_fn_02006768();
extern u32 native_fn_02006ce0();
extern u32 native_fn_02006d98();
extern u8 native_data_020e33c0[];
void native_main_0200670c(void *arg0, s32 arg1) {
    if (M2C_FIELD(native_data_020e33c0, s32 *, 0x1C) != 0) {
        native_fn_02006ce0(arg0, native_fn_02006768);
        M2C_FIELD(arg0, s32 *, 4) = arg1;
        M2C_FIELD(arg0, s32 *, 0) = (s32) (M2C_FIELD(arg0, s32 *, 0) | 0x80);
        M2C_FIELD(arg0, s32 *, 0x64) = 1;
        native_fn_02006d98(arg0);
        return;
    }
    native_fn_02006768(arg1);
}
