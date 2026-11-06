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
extern u32 native_arm7_data_04805f60;
extern u32 native_arm7_data_0380fff4;
u32 native_arm7_wram_037fa6c8(u32 arg0) {
    u32 var_r0;

    var_r0 = arg0;
    if (var_r0 >= (u32) &native_arm7_data_04805f60) {
        var_r0 -= M2C_FIELD(native_arm7_data_0380fff4, u16 *, 0x3DE);
    }
    return var_r0;
}
