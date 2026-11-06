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
extern u32 native_fn_0205f920();
extern u8 native_data_021c4968[];
extern u8 native_data_021c4970[];
extern u8 native_data_021c49b8[];
u32 native_main_02068d54(void) {
    if (M2C_FIELD(native_data_021c4968, s32 *, 0x24) != 0) {
        native_fn_0205f920(native_data_021c4970, 1, 2);
    }
    if (M2C_FIELD(native_data_021c4968, s32 *, 0x6C) != 0) {
        native_fn_0205f920(native_data_021c49b8, 1, 2);
    }
    if (M2C_FIELD(native_data_021c4968, u8 **, 0x98) == NULL) {
        return (u32) M2C_FIELD(native_data_021c4968, u8 **, 0x98);
    }
    native_fn_0205f920(M2C_FIELD(native_data_021c4968, u8 **, 0x98), 1, 2);
    native_fn_0202a498(2, M2C_FIELD(native_data_021c4968, u8 **, 0x98));
    M2C_FIELD(native_data_021c4968, u8 **, 0x98) = NULL;
    return (u32) native_data_021c4968;
}
