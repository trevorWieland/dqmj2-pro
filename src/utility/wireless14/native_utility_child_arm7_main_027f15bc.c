typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
extern u32 native_utility_child_arm7_data_0380fff4;
extern volatile u16 native_utility_child_arm7_data_04808080[];

void native_utility_child_arm7_main_027f15bc(void) {
    u8 *state = (u8 *)native_utility_child_arm7_data_0380fff4;
    native_utility_child_arm7_data_04808080[0] = 0;
    *(u16 *)(state + 0x4a4) = 0;
}
