typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef signed int s32;
extern u8 native_host_arm7_data_027f7884[];
extern u32 native_host_arm7_data_027f8884[];
u32 native_arm7_main_027e0564(u8 value) {
u8 *current;
u8 *base = native_host_arm7_data_027f7884;
s32 index = 0;
do {
current = base + index + 0x1000;
index++;
*(u8 *)(current + 0x554) = value;
} while (index < 32);
*(u32 *)((u8 *)native_host_arm7_data_027f8884 + 0x574) = 0;
return (u32)native_host_arm7_data_027f8884;
}
