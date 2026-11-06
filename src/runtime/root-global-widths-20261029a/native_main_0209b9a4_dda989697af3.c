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
extern u32 native_fn_0209a9e4();
extern u32 native_fn_0209bd94();
extern u32 native_fn_0209be60();
extern u32 native_fn_0209c05c();
extern u32 native_fn_0209e0fc();
extern u8 native_data_021d19e0[];
u32 native_main_0209b9a4(s32 arg0, u32 arg1, s32 arg2, s32 arg3, s32 arg4, s32 arg5) {
    if ((native_fn_0209a9e4() != 0) || (M2C_FIELD(*(u32 *)native_data_021d19e0, s32 *, 0x24) != 3)) {
        return 0U;
    }
    native_fn_0209bd94();
    M2C_FIELD(*(u32 *)native_data_021d19e0, s32 *, 0x80) = arg2;
    M2C_FIELD(*(u32 *)native_data_021d19e0, s32 *, 0x84) = arg3;
    native_fn_0209be60(5);
    native_fn_0209e0fc((u8) (arg0 - 1), arg1, native_fn_0209c05c, 0, arg4, arg5);
    return 1U;
}
