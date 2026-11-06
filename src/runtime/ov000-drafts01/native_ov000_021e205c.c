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
extern u32 native_fn_ov000_02218800();
extern u8 native_data_ov000_022322c4[];
u32 native_ov000_021e205c(void) {
    if ((M2C_FIELD(M2C_FIELD(native_data_ov000_022322c4, void **, 4), u16 *, 2) & 0x400) || (native_fn_ov000_02218800(2) != 0)) {
        return 1U;
    }
    return 0U;
}
