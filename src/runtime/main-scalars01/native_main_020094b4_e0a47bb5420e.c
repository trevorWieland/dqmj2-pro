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
extern u32 native_fn_02007074();
extern u32 native_fn_02009514();
extern u32 native_fn_02009c24();
extern u8 native_data_020e3760[];
extern u8 native_data_020e3764[];
u32 native_main_020094b4(void) {
    if (*(u32 *)native_data_020e3760 == 0) {
        goto block_2;
    }
    return *(u32 *)native_data_020e3760;
block_2:
    *(u32 *)native_data_020e3760 = 1;
    native_fn_02007074(native_data_020e3764);
    native_fn_02009514();
    return native_fn_02009c24();
}
