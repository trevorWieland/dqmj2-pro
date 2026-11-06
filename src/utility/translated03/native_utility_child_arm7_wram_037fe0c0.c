typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fe5e0(void);
u32 native_utility_child_arm7_wram_037fe0c0(u32 arg0, s32 arg1) {
    u32 temp_r5;
    u32 var_r0;

    var_r0 = arg0;
    temp_r5 = var_r0;
    if (arg1 == 0) {
        var_r0 = native_utility_child_arm7_arm_037fe5e0();
    }
    if (temp_r5 != 0) {
        M2C_FIELD(temp_r5, s32 *, 8) = arg1;
    }
    return var_r0;
}
