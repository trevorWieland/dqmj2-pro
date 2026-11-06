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
extern u32 native_fn_0204b178();
extern u32 native_fn_0205f98c();
void native_main_0204b5d4(void *arg0, s32 arg1) {
    u8 var_r4;

    if (M2C_FIELD(arg0, s32 *, 0x1C) == 0) {
        return;
    }
    var_r4 = 0;
    do {
        native_fn_0204b178(native_fn_0205f98c(M2C_FIELD(arg0, s32 *, 0x1C), var_r4), (u8) (arg1 + var_r4));
        var_r4 += 1;
    } while ((u32) var_r4 < 2U);
}
