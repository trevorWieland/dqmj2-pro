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
extern u32 native_fn_0205fa4c();
extern u32 native_fn_ov006_021e7d78();
extern u32 native_fn_ov006_021e7e28();
extern u32 native_fn_ov006_021e806c();
extern u32 native_fn_ov006_021e9130();
extern u8 native_data_ov006_02218d90[];
extern u8 native_data_ov006_02218e60[];
u32 native_ov006_021e9268(void) {
    native_fn_ov006_021e7d78();
    native_fn_ov006_021e9130();
    native_fn_0205fa4c(native_data_ov006_02218e60, 0);
    native_fn_ov006_021e806c();
    if (M2C_FIELD(native_data_ov006_02218d90, s32 *, 0x64) == 0) {
        native_fn_ov006_021e7e28();
    }
    M2C_FIELD(native_data_ov006_02218d90, s32 *, 4) = 0;
    return (u32) native_data_ov006_02218d90;
}
