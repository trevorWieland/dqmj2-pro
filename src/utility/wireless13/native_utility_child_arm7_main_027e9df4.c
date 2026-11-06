typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
extern u32 native_utility_child_arm7_data_0380fff4;

u32 native_utility_child_arm7_main_027e9df4(u32 bit) {
    return (1u << bit) & *(u16 *)((u8 *)native_utility_child_arm7_data_0380fff4 + 0x32c);
}
