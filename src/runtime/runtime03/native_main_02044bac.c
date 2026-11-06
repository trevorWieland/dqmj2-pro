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
extern u8 native_data_020f69ec[];
u32 native_main_02044bac(s32 arg0, u32 arg1) {
    u32 var_r2;

    var_r2 = 0;
    switch (arg1) {
    default:
        break;
    case 0:
        if (((u32) (M2C_FIELD(((arg0 * 0x64) + M2C_FIELD(native_data_020f69ec, s32 *, 4)), u8 *, 0x3E) << 0x1F) >> 0x1F) != 0) {
            var_r2 = 1;
        }
        break;
    case 1:
        if (((u32) (M2C_FIELD(((arg0 * 0x64) + M2C_FIELD(native_data_020f69ec, s32 *, 4)), u8 *, 0x3E) << 0x1E) >> 0x1F) != 0) {
            var_r2 = 1;
        }
        break;
    case 2:
        if (((u32) (M2C_FIELD(((arg0 * 0x64) + M2C_FIELD(native_data_020f69ec, s32 *, 4)), u8 *, 0x3E) << 0x1D) >> 0x1F) != 0) {
            var_r2 = 1;
        }
        break;
    case 3:
        if (((u32) (M2C_FIELD(((arg0 * 0x64) + M2C_FIELD(native_data_020f69ec, s32 *, 4)), u8 *, 0x3E) << 0x1C) >> 0x1F) != 0) {
            var_r2 = 1;
        }
        break;
    case 4:
        if (((u32) (M2C_FIELD(((arg0 * 0x64) + M2C_FIELD(native_data_020f69ec, s32 *, 4)), u8 *, 0x3E) << 0x1B) >> 0x1F) != 0) {
            var_r2 = 1;
        }
        break;
    case 5:
        if (((u32) (M2C_FIELD(((arg0 * 0x64) + M2C_FIELD(native_data_020f69ec, s32 *, 4)), u8 *, 0x3E) << 0x1A) >> 0x1F) != 0) {
            var_r2 = 1;
        }
        break;
    case 6:
        if (((u32) (M2C_FIELD(((arg0 * 0x64) + M2C_FIELD(native_data_020f69ec, s32 *, 4)), u8 *, 0x3E) << 0x19) >> 0x1F) != 0) {
            var_r2 = 1;
        }
        break;
    }
    return var_r2;
}
