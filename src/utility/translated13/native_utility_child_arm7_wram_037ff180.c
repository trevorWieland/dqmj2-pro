typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_data_03805898[];
u32 native_utility_child_arm7_wram_037ff180(void) {
    u32 temp_r0;

    temp_r0 = (0x19660D * *native_utility_child_arm7_data_03805898) + 0x3C6EF35F;
    *native_utility_child_arm7_data_03805898 = temp_r0;
    return (u32) (u16) (temp_r0 >> 0x10);
}
