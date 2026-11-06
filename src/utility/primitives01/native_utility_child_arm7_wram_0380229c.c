typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern u8 native_utility_child_arm7_data_038079a4[];
void native_utility_child_arm7_wram_0380229c(u32 value) {
    *(volatile u32 *)(native_utility_child_arm7_data_038079a4 + 0) = value;
}
