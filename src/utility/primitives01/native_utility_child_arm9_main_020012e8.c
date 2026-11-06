typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern u8 native_utility_child_arm9_data_02022620[];
void native_utility_child_arm9_main_020012e8(u32 value) {
    *(volatile u8 *)(native_utility_child_arm9_data_02022620 + 2) = value;
}
