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
extern u32 native_fn_ov001_021db8d0();
extern u32 native_fn_ov001_021dbcf0();
extern u32 native_fn_ov001_0220f960();
extern u8 native_data_ov001_0223e0d8[];
u32 native_ov001_0220e0c8(void) {
    if ((native_fn_ov001_021db8d0(M2C_FIELD(native_data_ov001_0223e0d8, void **, 0xC)) != 0) && ((s32) native_fn_ov001_0220f960(M2C_FIELD(M2C_FIELD(native_data_ov001_0223e0d8, void **, 0xC), s32 *, 0x1E8) + 0x46, native_fn_ov001_021dbcf0(M2C_FIELD(native_data_ov001_0223e0d8, void **, 0xC))) > 0)) {
        M2C_FIELD(native_data_ov001_0223e0d8, s8 *, 2) = 8;
    } else {
        M2C_FIELD(native_data_ov001_0223e0d8, s8 *, 2) = 3;
    }
    return 1U;
}
