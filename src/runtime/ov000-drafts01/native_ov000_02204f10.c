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
extern u32 native_fn_02061d08();
extern u32 native_fn_0206e428();
extern u8 native_data_ov000_02238190[];
u32 native_ov000_02204f10(void) {
    if (M2C_FIELD(native_data_ov000_02238190, u8 *, 6) == 0) {
        return (u32) M2C_FIELD(native_data_ov000_02238190, u8 *, 6);
    }
    native_fn_0206e428();
    native_fn_02061d08(3, 1);
    native_fn_02061d08(0, 1);
    native_fn_02061d08(1, 1);
    native_fn_02061d08(2, 1);
    M2C_FIELD(native_data_ov000_02238190, u8 *, 6) = 0U;
    return (u32) native_data_ov000_02238190;
}
