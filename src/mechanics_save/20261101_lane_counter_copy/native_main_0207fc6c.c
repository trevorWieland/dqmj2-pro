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
extern u32 native_fn_02008e0c(const void *, void *, u32);
extern u32 native_fn_0205e7a8(s32, s32);
extern u32 native_fn_02081168(u32);
extern u8 native_data_020de57c[];
extern u8 native_data_021c6d80[];
extern u8 native_data_021c6d88[];
u32 native_main_0207fc6c(const u8 *arg0) {
    u8 temp_r3;

    if ((u32) *native_data_021c6d80 >= (u32) M2C_FIELD(native_data_020de57c, u8 *, 1)) {
        *native_data_021c6d80 = M2C_FIELD(native_data_020de57c, u8 *, 1) - 1;
    }
    native_fn_02008e0c(arg0, native_data_021c6d88 + (*native_data_021c6d80 * 3), 3);
    if ((u32) ++*native_data_021c6d80 >= (u32) M2C_FIELD(native_data_020de57c, u8 *, 1)) {
        native_fn_02081168(9);
    }
    native_fn_0205e7a8(-1, 0x52);
    M2C_FIELD(native_data_020de57c, u8 *, 0) = 1;
    return (u32) native_data_020de57c;
}
