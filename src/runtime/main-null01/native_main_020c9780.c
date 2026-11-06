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
extern u32 native_fn_0202a498();
extern u32 native_fn_020484dc();
extern u32 native_fn_020485b4();
extern u32 native_fn_0204861c();
extern u32 native_fn_0205f920();
extern u32 native_fn_02068d54();
extern u32 native_fn_ov000_021f2940();
extern u8 native_data_021d64b8[];
u32 native_main_020c9780(void) {
    if (M2C_FIELD(native_data_021d64b8, void **, 0x10) != NULL) {
        native_fn_0204861c(1, M2C_FIELD(M2C_FIELD(native_data_021d64b8, void **, 0x10), u8 *, 0x81));
        native_fn_0202a498(2, M2C_FIELD(native_data_021d64b8, void **, 0x10));
        M2C_FIELD(native_data_021d64b8, void **, 0x10) = NULL;
    }
    if (M2C_FIELD(native_data_021d64b8, s32 *, 8) != 0) {
        native_fn_ov000_021f2940();
        native_fn_020485b4(M2C_FIELD(native_data_021d64b8, s32 *, 8));
    }
    if (M2C_FIELD(native_data_021d64b8, void **, 4) != NULL) {
        native_fn_0205f920(M2C_FIELD(native_data_021d64b8, void **, 4), 1, 2);
        native_fn_0202a498(2, M2C_FIELD(native_data_021d64b8, void **, 4));
        M2C_FIELD(native_data_021d64b8, void **, 4) = NULL;
    }
    native_fn_02068d54();
    return native_fn_020484dc(1, M2C_FIELD(native_data_021d64b8, u8 *, 0));
}
