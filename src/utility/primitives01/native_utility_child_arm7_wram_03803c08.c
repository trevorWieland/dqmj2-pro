typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern u8 native_utility_child_arm7_data_038081a8[];
u32 native_utility_child_arm7_wram_03803c08(void) {
    return *(volatile u32 *)(native_utility_child_arm7_data_038081a8 + 0);
}
