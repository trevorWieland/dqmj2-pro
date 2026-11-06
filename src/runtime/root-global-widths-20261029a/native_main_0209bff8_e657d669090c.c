#define NULL ((void *)0)
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
extern u32 native_fn_0209be60();
extern u32 native_fn_0209d1a8();
extern u8 native_data_021d19e0[];
u32 native_main_0209bff8(s32 arg0, s32 arg1) {
    u8 *(*temp_r3)(s32, s32, s32);
    u8 *var_r0;

    if (arg0 == 0) {
        M2C_FIELD(*(u32 *)native_data_021d19e0, s32 *, 0x64) = arg1;
        native_fn_0209be60(3);
        native_fn_0209d1a8();
    } else {
        native_fn_0209be60(0);
    }
    var_r0 = native_data_021d19e0;
    temp_r3 = M2C_FIELD(*(u32 *)native_data_021d19e0, u8 *(**)(s32, s32, s32), 0x70);
    if (temp_r3 != NULL) {
        var_r0 = temp_r3(arg0, arg1, M2C_FIELD(*(u32 *)native_data_021d19e0, s32 *, 0x74));
    }
    return (u32) var_r0;
}
