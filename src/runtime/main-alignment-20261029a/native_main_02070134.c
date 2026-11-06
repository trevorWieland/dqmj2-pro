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
extern u32 native_fn_02045dc4();
extern u32 native_fn_0206fddc();
extern u8 native_data_021c5004[] __attribute__((aligned(2)));
u32 native_main_02070134(void) {
    native_fn_0206fddc();
    if (((s32) (M2C_FIELD(native_data_021c5004, s8 *, 0xD1) << 0x1C) >> 0x1F) != 0) {
        M2C_FIELD(native_data_021c5004, s8 *, 0xD1) = (s8) (M2C_FIELD(native_data_021c5004, s8 *, 0xD1) & ~8);
        native_fn_02045dc4(0, 1, 0x1A, 8, 5, 0xF);
        native_fn_02045dc4(0, 2, 0x1A, 8, 5, 0xF);
    }
    M2C_FIELD(native_data_021c5004, s8 *, 0xD1) = (s8) (M2C_FIELD(native_data_021c5004, s8 *, 0xD1) & ~4);
    M2C_FIELD(native_data_021c5004, s8 *, 0xD1) = (s8) (M2C_FIELD(native_data_021c5004, s8 *, 0xD1) | 2);
    return (u32) native_data_021c5004;
}
