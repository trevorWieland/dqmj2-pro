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
extern u32 native_fn_02061944();
extern u32 native_fn_02065818();
extern u8 native_data_021c4f60[];
u32 native_main_0206e160(s32 arg0, u32 arg1, u32 arg2) {
    u32 temp_r0;

    temp_r0 = native_fn_02061944();
    if (arg0 != 0) {
        return temp_r0;
    }
    if ((M2C_FIELD(native_data_021c4f60, void **, 0x20) != NULL) && (M2C_FIELD(M2C_FIELD(native_data_021c4f60, void **, 0x20), u8 *, 0x1D) != 0)) {
        return native_fn_02065818(temp_r0 + 0x10, arg1, arg2);
    }
    return temp_r0;
}
