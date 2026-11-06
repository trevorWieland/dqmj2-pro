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
extern u32 native_fn_0202a498();
extern u32 native_fn_020484dc();
extern u32 native_fn_020485b4();
extern u32 native_fn_0204861c();
extern u32 native_fn_0205f920();
extern u8 native_data_ov003_021e0d18[];
u32 native_ov003_021dfbf4(void) {
    if (M2C_FIELD(native_data_ov003_021e0d18, void **, 0xC) != NULL) {
        native_fn_0204861c(1, M2C_FIELD(M2C_FIELD(native_data_ov003_021e0d18, void **, 0xC), u8 *, 0x81));
        native_fn_0202a498(2, M2C_FIELD(native_data_ov003_021e0d18, void **, 0xC));
        M2C_FIELD(native_data_ov003_021e0d18, void **, 0xC) = NULL;
    }
    if (M2C_FIELD(native_data_ov003_021e0d18, s32 *, 0x1C) != 0) {
        native_fn_020485b4();
    }
    if (M2C_FIELD(native_data_ov003_021e0d18, void **, 0x14) != NULL) {
        native_fn_0205f920(M2C_FIELD(native_data_ov003_021e0d18, void **, 0x14), 1, 2);
        native_fn_0202a498(2, M2C_FIELD(native_data_ov003_021e0d18, void **, 0x14));
        M2C_FIELD(native_data_ov003_021e0d18, void **, 0x14) = NULL;
    }
    if (M2C_FIELD(native_data_ov003_021e0d18, void **, 0x10) != NULL) {
        native_fn_0205f920(M2C_FIELD(native_data_ov003_021e0d18, void **, 0x10), 1, 2);
        native_fn_0202a498(2, M2C_FIELD(native_data_ov003_021e0d18, void **, 0x10));
        M2C_FIELD(native_data_ov003_021e0d18, void **, 0x10) = NULL;
    }
    return native_fn_020484dc(1, M2C_FIELD(native_data_ov003_021e0d18, u8 *, 0));
}
