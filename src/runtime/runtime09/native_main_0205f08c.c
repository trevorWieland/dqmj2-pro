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
extern u32 native_fn_020391e4();
extern u32 native_fn_0205ed58();
extern u32 native_fn_0205ef60();
extern u32 native_fn_0205ef8c();
extern u32 native_fn_0205f088();
extern u8 native_data_021b8ae0[];
u32 native_main_0205f08c(u32 arg0, u32 arg1) {
    if (native_fn_0205ef60() == 0) {
        goto block_4;
    }
    if (native_fn_020391e4(arg0, native_fn_0205f088(arg1), M2C_FIELD(native_data_021b8ae0, s32 *, 4)) == 0) {
        goto block_3;
    }
    return native_fn_0205ed58(0);
block_3:
    native_fn_0205ef8c(arg0);
    return native_fn_0205ed58(5);
block_4:
    return native_fn_0205ed58(4);
}
