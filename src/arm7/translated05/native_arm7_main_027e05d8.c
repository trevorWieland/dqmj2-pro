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
extern u32 native_arm7_data_027f8884;
u32 native_arm7_main_027e05d8(u32 arg0) {
    u32 var_r0;

    if (M2C_FIELD(M2C_FIELD(&native_arm7_data_027f8884, void **, 0x54C), u8 *, 0x53) == 8) {
        if (arg0 < 0x16U) {
            return 0U;
        }
        if (arg0 < 0x1CU) {
            return 1U;
        }
        if (arg0 < 0x22U) {
            var_r0 = 2;
        } else {
            var_r0 = 3;
        }
        return var_r0;
    }
    if (arg0 < 8U) {
        return 0U;
    }
    if (arg0 < 0xEU) {
        return 1U;
    }
    if (arg0 < 0x14U) {
        return 2U;
    }
    return 3U;
}
