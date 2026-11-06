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
extern u32 native_fn_0209ad08();
extern u8 native_data_021d19bc[];
u32 native_main_0209ac24(void) {
    if (M2C_FIELD(native_data_021d19bc, void **, 4) == NULL) {
        return 0U;
    }
    if (M2C_FIELD(M2C_FIELD(native_data_021d19bc, void **, 4), s32 *, 0) != 0) {
        M2C_FIELD(M2C_FIELD(native_data_021d19bc, void **, 4), s16 *, 4) = 3;
        native_fn_0209ad08();
        if (M2C_FIELD(M2C_FIELD(native_data_021d19bc, void **, 4), u8 *, 0xC) != 0) {
            return 1U;
        }
        return 0U;
    }
    return 0U;
}
