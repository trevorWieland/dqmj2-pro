typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
extern u16 native_utility_child_arm7_crc_table16_027f7f74[16];
u32 native_utility_child_arm7_main_027e93d4(s32 byte, s32 previous) {
    u16 value;
    u32 previousLookup = native_utility_child_arm7_crc_table16_027f7f74[previous & 15];
    value = previousLookup ^
        (u16)(0xFFF & (previous >> 4)) ^ native_utility_child_arm7_crc_table16_027f7f74[byte & 15];
    return (u16)(native_utility_child_arm7_crc_table16_027f7f74[value & 15] ^
        (u16)(0xFFF & ((s32)value >> 4)) ^ native_utility_child_arm7_crc_table16_027f7f74[(byte >> 4) & 15]);
}
