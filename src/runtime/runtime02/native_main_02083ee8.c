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
extern u8 native_data_021c72a0[];
u32 native_main_02083ee8(void) {
    s32 temp_r1;
    u32 var_r0;

    temp_r1 = ((M2C_FIELD(native_data_021c72a0, u16 *, 6) * (M2C_FIELD(native_data_021c72a0, u8 *, 3) + 1)) + 0x59) & ~0x1F;
    var_r0 = ((((M2C_FIELD(native_data_021c72a0, u16 *, 6) + 0xE) * M2C_FIELD(native_data_021c72a0, u8 *, 3)) + 0x29) & ~0x1F) * 2;
    if (var_r0 < (u32) (temp_r1 * 2)) {
        var_r0 = temp_r1 * 2;
    }
    return var_r0;
}
