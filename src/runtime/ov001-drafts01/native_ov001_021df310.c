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
extern u32 native_fn_ov001_021e9640();
extern u8 native_data_ov001_022388ec[];
u32 native_ov001_021df310(void) {
    if ((M2C_FIELD(native_data_ov001_022388ec, u16 *, 0x36) == 0xD9) && (M2C_FIELD(M2C_FIELD(native_data_ov001_022388ec, void **, 0x48), s8 *, 0x237) != 0)) {
        native_fn_ov001_021e9640(1);
    } else {
        native_fn_ov001_021e9640(0);
    }
    M2C_FIELD(native_data_ov001_022388ec, s8 *, 8) = 6;
    return 1U;
}
