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
extern u32 native_arm7_data_027ffc00;
u32 native_arm7_wram_037fe3ec(s32 arg0, s32 arg1) {
    u32 var_r3;

    var_r3 = 1;
    if (!(M2C_FIELD(&(&native_arm7_data_027ffc00)[arg1], s32 *, 0x388) & (1 << arg0))) {
        var_r3 = 0;
    }
    return var_r3;
}
