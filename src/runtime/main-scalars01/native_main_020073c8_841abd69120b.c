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
extern u32 native_fn_02007560();
extern u32 native_fn_02007644();
extern u32 native_fn_020076ec();
extern u32 native_fn_02007700();
extern u8 native_data_020e363c[];
u32 native_main_020073c8(void) {
    if (*(u32 *)native_data_020e363c == 0) {
        goto block_2;
    }
    return *(u32 *)native_data_020e363c;
block_2:
    *(u32 *)native_data_020e363c = 1;
    native_fn_020076ec(0, native_fn_02007560(0));
    native_fn_02007700(0, native_fn_02007644(0));
    native_fn_02007700(2, 0U);
    native_fn_020076ec(2, 0U);
    native_fn_020076ec(3, native_fn_02007560(3));
    native_fn_02007700(3, native_fn_02007644(3));
    native_fn_020076ec(4, native_fn_02007560(4));
    native_fn_02007700(4, native_fn_02007644(4));
    native_fn_020076ec(5, native_fn_02007560(5));
    native_fn_02007700(5, native_fn_02007644(5));
    native_fn_020076ec(6, native_fn_02007560(6));
    return native_fn_02007700(6, native_fn_02007644(6));
}
