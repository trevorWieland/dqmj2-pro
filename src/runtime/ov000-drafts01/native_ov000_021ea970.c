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
extern u32 native_fn_0203ca5c();
extern u32 native_fn_0203caa4();
extern u32 native_fn_02040820();
extern u32 native_fn_ov000_021dff00();
extern u8 native_data_ov000_02236950[];
u32 native_ov000_021ea970(void) {
    if ((M2C_FIELD(M2C_FIELD(native_data_ov000_02236950, void **, 0x18), s16 *, 0x1F0) != 0) && (M2C_FIELD(M2C_FIELD(native_data_ov000_02236950, void **, 0x18), u8 *, 0x160) != 0)) {
        native_fn_ov000_021dff00();
        native_fn_0203caa4(M2C_FIELD(native_data_ov000_02236950, void **, 0xC), 0x41);
        native_fn_0203caa4(M2C_FIELD(native_data_ov000_02236950, void **, 0x18), 0x41);
    }
    if ((M2C_FIELD(M2C_FIELD(native_data_ov000_02236950, void **, 0x20), s32 *, 0x30) == 0) && (M2C_FIELD(native_data_ov000_02236950, u8 *, 7) == 0)) {

    } else {
        native_fn_0203ca5c(M2C_FIELD(native_data_ov000_02236950, s32 *, 8), 0);
        M2C_FIELD(native_data_ov000_02236950, u8 *, 7) = 0U;
    }
    return native_fn_02040820();
}
