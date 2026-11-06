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
extern u8 native_data_ov000_0222f850[];
extern u8 native_data_ov000_02243e3c[];
u32 native_ov000_02213cdc(s32 arg0) {
    s32 temp_r2;
    s32 var_r0;
    u32 var_r1;
    u8 temp_r0;

    var_r0 = arg0;
    var_r1 = 0;
    if (var_r0 < 0) {
        var_r0 = (s32) (s8) *native_data_ov000_0222f850;
    }
    if (var_r0 >= 0) {
        temp_r2 = (var_r0 * 0x10C) + (s32) native_data_ov000_02243e3c;
        if (M2C_FIELD(temp_r2, u8 *, 0x105) != 0) {
            temp_r0 = M2C_FIELD(temp_r2, u8 *, 0x106);
            switch (temp_r0) {
            default:
                break;
            case 0:
            case 8:
            case 9:
            case 10:
            case 11:
            case 12:
            case 13:
            case 14:
            case 15:
            case 16:
                if (M2C_FIELD(temp_r2, u8 *, 0x107) == 0) {
                    var_r1 = 1;
                    M2C_FIELD(temp_r2, u8 *, 0x107) = 1U;
                }
                break;
            case 1:
                if (M2C_FIELD(temp_r2, u8 *, 0x107) == 0) {
                    var_r1 = 1;
                    M2C_FIELD(temp_r2, u8 *, 0x107) = 1U;
                }
                break;
            case 2:
                if (M2C_FIELD(temp_r2, u8 *, 0x107) == 0) {
                    var_r1 = 1;
                    M2C_FIELD(temp_r2, u8 *, 0x107) = 1U;
                }
                break;
            case 3:
                if (M2C_FIELD(temp_r2, u8 *, 0x107) == 0) {
                    var_r1 = 1;
                    M2C_FIELD(temp_r2, u8 *, 0x107) = 1U;
                }
                break;
            case 4:
                if (M2C_FIELD(temp_r2, u8 *, 0x107) == 0) {
                    var_r1 = 1;
                    M2C_FIELD(temp_r2, u8 *, 0x107) = 1U;
                }
                break;
            case 6:
                if (M2C_FIELD(temp_r2, u8 *, 0x107) == 0) {
                    var_r1 = 1;
                    M2C_FIELD(temp_r2, u8 *, 0x107) = 1U;
                }
                break;
            case 7:
                if (M2C_FIELD(temp_r2, u8 *, 0x107) == 0) {
                    var_r1 = 1;
                    M2C_FIELD(temp_r2, u8 *, 0x107) = 1U;
                }
                break;
            case 17:
                if (M2C_FIELD(temp_r2, u8 *, 0x107) == 0) {
                    var_r1 = 1;
                    M2C_FIELD(temp_r2, u8 *, 0x107) = 1U;
                }
                break;
            }
        }
    }
    return var_r1;
}
