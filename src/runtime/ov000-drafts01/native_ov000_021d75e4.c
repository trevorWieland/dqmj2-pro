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
extern u32 native_fn_02048644();
extern u32 native_fn_02048a60();
extern u32 native_fn_02048a94();
extern u32 native_fn_02048a9c();
extern u32 native_fn_ov000_021d7da4();
typedef struct {
    u8 unknown_0[0x20];
    s32 field_20;
} Record_native_data_ov000_022300c0;
extern Record_native_data_ov000_022300c0 native_data_ov000_022300c0;
u32 native_ov000_021d75e4(void *arg0, u32 arg1, u32 arg2, u32 arg3, u8 arg4, u8 arg5) {
    u32 temp_r0;

    native_fn_ov000_021d7da4();
    native_fn_02048a9c(arg0, arg4);
    native_fn_02048a94(arg0, arg5);
    native_fn_02048a60(arg0, arg1, arg2);
    native_fn_02048644(arg0, native_data_ov000_022300c0.field_20, arg3);
    temp_r0 = M2C_FIELD(arg0, u32 *, 0x7C) & ~2;
    M2C_FIELD(arg0, u32 *, 0x7C) = temp_r0;
    return temp_r0;
}
