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
extern u32 native_fn_ov001_021e865c();
extern u32 native_fn_ov001_02216ac4();
extern u8 native_data_ov001_02242c40[];
u32 native_ov001_02217d68(void) {
    if (native_fn_ov001_02216ac4(M2C_FIELD(native_data_ov001_02242c40, void **, 8), M2C_FIELD(native_data_ov001_02242c40, u8 *, 1), 0) != 0) {
        M2C_FIELD(native_data_ov001_02242c40, u8 *, 0) = 3;
        native_fn_ov001_021e865c(M2C_FIELD(M2C_FIELD(native_data_ov001_02242c40, void **, 8), u8 *, 0x31E), M2C_FIELD(M2C_FIELD(native_data_ov001_02242c40, void **, 8), u8 *, 0x31F));
    }
    return 0U;
}
