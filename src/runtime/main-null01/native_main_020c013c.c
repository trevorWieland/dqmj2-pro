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
extern u32 native_fn_0204861c();
extern u8 native_data_021d4bec[];
u32 native_main_020c013c(void) {
    if (M2C_FIELD(native_data_021d4bec, void **, 0x18) != NULL) {
        native_fn_0204861c(1, M2C_FIELD(M2C_FIELD(native_data_021d4bec, void **, 0x18), u8 *, 0x81));
        native_fn_0202a498(2, M2C_FIELD(native_data_021d4bec, void **, 0x18));
        M2C_FIELD(native_data_021d4bec, void **, 0x18) = NULL;
    }
    if (M2C_FIELD(native_data_021d4bec, void **, 0xC) != NULL) {
        native_fn_0204861c(1, M2C_FIELD(M2C_FIELD(native_data_021d4bec, void **, 0xC), u8 *, 0x81));
        native_fn_0202a498(2, M2C_FIELD(native_data_021d4bec, void **, 0xC));
        M2C_FIELD(native_data_021d4bec, void **, 0xC) = NULL;
    }
    if (M2C_FIELD(native_data_021d4bec, void **, 0x1C) == NULL) {
        return (u32) M2C_FIELD(native_data_021d4bec, void **, 0x1C);
    }
    native_fn_0204861c(1, M2C_FIELD(M2C_FIELD(native_data_021d4bec, void **, 0x1C), u8 *, 0x81));
    native_fn_0202a498(2, M2C_FIELD(native_data_021d4bec, void **, 0x1C));
    M2C_FIELD(native_data_021d4bec, void **, 0x1C) = NULL;
    return (u32) native_data_021d4bec;
}
