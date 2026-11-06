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
extern u32 native_fn_020a4034(u32 arg0, u32 arg1, u32 arg2);
extern u32 native_fn_020a40a4(u32);
extern u32 native_fn_020baa7c();
extern u8 native_data_021d3044[];

u32 native_main_020baaf0(u32 arg0, u32 arg1, u32 arg2, s32 arg3) {
    u32 result;
    if ((M2C_FIELD(native_data_021d3044, s32 *, 0xC) == 6) && (native_fn_020a40a4((u32)native_fn_020baa7c) != 0)) {
        M2C_FIELD(native_data_021d3044, s32 *, 0x24) = arg3;
        M2C_FIELD(native_data_021d3044, u32 *, 0x18) = arg0;
        M2C_FIELD(native_data_021d3044, s32 *, 0x28) = 0;
        M2C_FIELD(native_data_021d3044, s32 *, 0xC) = 7;
        result = native_fn_020a4034(arg0, arg1, arg2);
        if (result == arg0) {
            return 1U;
        }
        M2C_FIELD(native_data_021d3044, s32 *, 0x24) = 0;
        M2C_FIELD(native_data_021d3044, u32 *, 0x18) = 0U;
        M2C_FIELD(native_data_021d3044, s32 *, 0x28) = 0;
        M2C_FIELD(native_data_021d3044, s32 *, 0xC) = 6;
        return 0U;
    }
    return 0U;
}
