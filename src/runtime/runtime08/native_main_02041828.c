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
extern u32 native_fn_020414e0();
extern u32 native_fn_02041598();
u32 native_main_02041828(u32 arg0, s32 arg1) {
    u32 temp_r0;

    switch (arg1) {
    case 0:
        native_fn_020414e0(arg0, 0, 2, 1);
        break;
    case 2:
        native_fn_020414e0(arg0, 1, 2, 1);
        break;
    case 3:
        native_fn_020414e0(arg0, 1, 3, 1);
        break;
    }
    do {
        temp_r0 = native_fn_02041598(arg0);
    } while (temp_r0 == 0);
    return temp_r0;
}
