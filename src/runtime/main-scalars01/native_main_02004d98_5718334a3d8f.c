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
extern u32 native_fn_02003ff4();
extern u32 native_fn_0200854c();
extern u32 native_fn_02008bf8();
extern u8 native_data_020dcb44[];
u32 native_main_02004d98(u32 arg0, s32 arg1, u32 arg2) {
    u32 temp_ip;

    temp_ip = native_fn_02003ff4();
    if (*(u32 *)native_data_020dcb44 == -1) {
        goto block_3;
    }
    if (arg2 <= 0x1CU) {
        goto block_3;
    }
    return native_fn_0200854c(*(u32 *)native_data_020dcb44, arg0, temp_ip + arg1, arg2);
block_3:
    return native_fn_02008bf8(arg0, temp_ip + arg1, arg2);
}
