typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
extern u32 native_arm7_data_0380fff4;

u32 native_arm7_main_027ebfec(u32 index) {
    u8 *records = *(u8 **)((u8 *)native_arm7_data_0380fff4 + 0x31c);
    return *(u16 *)(records + index * 28);
}
