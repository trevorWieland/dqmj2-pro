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
extern u32 native_fn_020044ac();
extern u32 native_fn_020045d8();
extern u32 native_fn_0203d0fc();
extern u32 native_fn_02041764();
extern u32 native_fn_0204176c();
extern u32 native_fn_0205e1d0();
extern u32 native_fn_0205e1fc();
extern u32 native_fn_0205e234();
extern u32 native_fn_0205e25c();
extern u32 native_fn_0205e294();
extern u32 native_fn_ov000_021f3904();
extern u32 native_fn_ov000_0222a758();
extern u8 native_data_02106950[];
u32 native_main_0205e2d0(void) {
    u32 temp_r4;
    u32 temp_r5;
    u32 var_r6;

    var_r6 = 4;
    temp_r5 = native_fn_0203d0fc();
    temp_r4 = native_fn_ov000_0222a758();
    native_fn_020044ac();
    native_fn_020045d8();
    if ((temp_r5 == 0) || (temp_r4 != 0)) {
        switch (M2C_FIELD(native_data_02106950, s8 *, 1)) {
        case 0:
            native_fn_0205e1d0();
            break;
        case 1:
            native_fn_0205e1fc();
            break;
        case 2:
            var_r6 = native_fn_0205e234();
            break;
        }
        native_fn_0205e25c();
    } else if (temp_r5 == 2) {
        native_fn_ov000_021f3904();
    }
    native_fn_0205e294();
    native_fn_02041764();
    native_fn_0204176c();
    return var_r6;
}
