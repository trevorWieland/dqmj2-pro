typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

u32 native_utility_child_arm7_wram_03802908(u32 arg0) {
    u32 temp_r1;
    u32 temp_r1_2;
    u32 temp_r1_3;
    u32 temp_r1_4;

    temp_r1_2 = arg0 - ((arg0 >> 1) & 0x55555555);
    temp_r1_3 = (temp_r1_2 & 0x33333333) + ((temp_r1_2 >> 2) & 0x33333333);
    temp_r1_4 = (temp_r1_3 + (temp_r1_3 >> 4)) & 0x0F0F0F0F;
    temp_r1 = temp_r1_4 + (temp_r1_4 >> 8);
    return (u32) (u8) (temp_r1 + (temp_r1 >> 0x10));
}
