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
extern u32 native_fn_020451c4(const void *, u32, u32, u32 *);
extern u8 native_data_020ddab0[];
extern u8 native_data_020ddac8[];
extern u8 native_data_020ddae0[];
extern u8 native_data_020ddaf4[];
extern u8 native_data_020faaec[];
u32 native_main_02046188(s32 arg0, u32 arg1, u32 arg2) {
    s32 temp_r4;
    u32 selector;

    temp_r4 = (arg0 * 0x14) + (s32) native_data_020faaec;
    M2C_FIELD(temp_r4, u32 *, 8) = 0U;
    M2C_FIELD(temp_r4, s32 *, 0xC) = 0;
    M2C_FIELD(temp_r4, u8 *, 0x10) = arg1;
    selector = (arg1 & 255U);
    switch (selector) {
    case 1:
        if (M2C_FIELD(temp_r4, u32 *, 0) == 0) {
            M2C_FIELD(temp_r4, u32 *, 0) = native_fn_020451c4(native_data_020ddab0, 0, arg2, temp_r4 + 8);
        }
        if (M2C_FIELD(temp_r4, u32 *, 4) == 0) {
            M2C_FIELD(temp_r4, u32 *, 4) = native_fn_020451c4(native_data_020ddac8, 1, arg2, temp_r4 + 0xC);
        }
        break;
    case 2:
        if (M2C_FIELD(temp_r4, u32 *, 0) == 0) {
            M2C_FIELD(temp_r4, u32 *, 0) = native_fn_020451c4(native_data_020ddae0, 0x10, arg2, temp_r4 + 8);
        }
        break;
    default:
    case 0:
        if (M2C_FIELD(temp_r4, u32 *, 0) == 0) {
            M2C_FIELD(temp_r4, u32 *, 0) = native_fn_020451c4(native_data_020ddaf4, 0xF, arg2, temp_r4 + 8);
        }
        break;
    }
    return M2C_FIELD(temp_r4, u32 *, 8);
}
