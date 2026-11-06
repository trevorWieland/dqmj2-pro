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
extern u32 native_fn_02048a60();
extern u32 native_fn_0205f98c();
extern u8 native_data_ov000_02236da4[];
u32 native_ov000_021f2ab8(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    native_fn_02048a60(native_fn_0205f98c(M2C_FIELD(M2C_FIELD(native_data_ov000_02236da4, void **, 0x14), s32 *, 0x1C), 0), arg0, arg1);
    return native_fn_02048a60(native_fn_0205f98c(M2C_FIELD(M2C_FIELD(native_data_ov000_02236da4, void **, 0x14), s32 *, 0x1C), 1), arg2, arg3);
}
