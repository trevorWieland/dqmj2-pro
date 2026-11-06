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
extern u32 native_fn_0205f98c();
extern u8 native_data_ov000_02236bd0[];
u32 native_ov000_021ef1cc(s32 arg0) {
    if (arg0 == 0) {
        M2C_FIELD(M2C_FIELD(native_data_ov000_02236bd0, void **, 0xC), s32 *, 0x7C) = (s32) (M2C_FIELD(M2C_FIELD(native_data_ov000_02236bd0, void **, 0xC), s32 *, 0x7C) & ~2);
        native_fn_02048644(native_fn_0205f98c(M2C_FIELD(M2C_FIELD(native_data_ov000_02236bd0, void **, 0x10), s32 *, 0x1C), 0), M2C_FIELD(native_data_ov000_02236bd0, s32 *, 0x18), 0x15);
        return native_fn_02048644(native_fn_0205f98c(M2C_FIELD(M2C_FIELD(native_data_ov000_02236bd0, void **, 0x10), s32 *, 0x1C), 1), M2C_FIELD(native_data_ov000_02236bd0, s32 *, 0x18), 0x16);
    }
    M2C_FIELD(M2C_FIELD(native_data_ov000_02236bd0, void **, 0xC), s32 *, 0x7C) = (s32) (M2C_FIELD(M2C_FIELD(native_data_ov000_02236bd0, void **, 0xC), s32 *, 0x7C) | 2);
    native_fn_02048644((u32) M2C_FIELD(native_data_ov000_02236bd0, void **, 0xC), M2C_FIELD(native_data_ov000_02236bd0, s32 *, 0x18), 0x2D);
    native_fn_02048644(native_fn_0205f98c(M2C_FIELD(M2C_FIELD(native_data_ov000_02236bd0, void **, 0x10), s32 *, 0x1C), 0), M2C_FIELD(native_data_ov000_02236bd0, s32 *, 0x18), 0x3C);
    return native_fn_02048644(native_fn_0205f98c(M2C_FIELD(M2C_FIELD(native_data_ov000_02236bd0, void **, 0x10), s32 *, 0x1C), 1), M2C_FIELD(native_data_ov000_02236bd0, s32 *, 0x18), 0x3D);
}
