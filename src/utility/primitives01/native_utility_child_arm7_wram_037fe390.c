typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern u8 native_utility_child_arm7_data_03805b74[];
u32 native_utility_child_arm7_wram_037fe390(void) {
    return *(volatile u16 *)(native_utility_child_arm7_data_03805b74 + 0);
}
