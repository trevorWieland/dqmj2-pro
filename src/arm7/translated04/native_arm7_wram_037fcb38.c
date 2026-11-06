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
extern u32 native_arm7_data_027f91ec;
extern u32 native_arm7_data_0380b4e4;
u32 native_arm7_wram_037fcb38(s32 arg0) {
    u32 *var_r0;
    u32 *var_r0_2;

    switch (arg0) {
    case 1:
        return (u32) &native_arm7_data_027f91ec;
    case 7:
        var_r0 = &native_arm7_data_0380b4e4;
        if ((u32) &native_arm7_data_0380b4e4 > 0x03800000U) {
            var_r0 = (u32 *)0x03800000;
        }
        return (u32) var_r0;
    case 8:
        var_r0_2 = (u32 *)0x03800000;
        if ((u32) &native_arm7_data_0380b4e4 > 0x03800000U) {
            var_r0_2 = &native_arm7_data_0380b4e4;
        }
        return (u32) var_r0_2;
    default:
        return 0U;
    }
}
