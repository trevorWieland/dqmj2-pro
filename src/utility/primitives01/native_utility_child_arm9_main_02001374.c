typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern u8 native_utility_child_arm9_data_02026600[];
void native_utility_child_arm9_main_02001374(u32 value) {
    *(volatile u32 *)(native_utility_child_arm9_data_02026600 + 12) = value;
}
