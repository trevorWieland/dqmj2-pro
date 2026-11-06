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
extern u32 native_fn_020c0a6c();
extern u8 native_data_021c4968[];
extern u8 native_data_021c4a0e[];
u32 native_main_02068ef8(u8 arg0, s8 arg1, s8 arg2, s8 arg3, s32 arg4) {
    M2C_FIELD(native_data_021c4968, u8 *, 0) = arg0;
    M2C_FIELD(native_data_021c4968, s8 *, 2) = arg1;
    M2C_FIELD(native_data_021c4968, s8 *, 3) = arg2;
    if (arg3 == -1) {
        return (u32) arg0;
    }
    M2C_FIELD(native_data_021c4968, s8 *, 5) = arg3;
    M2C_FIELD(native_data_021c4968, s8 *, 4) = 1;
    *(native_data_021c4a0e + (arg3 * 0x10)) = 1;
    return native_fn_020c0a6c(arg4);
}
