typedef unsigned short u16;
typedef unsigned char u8;
typedef unsigned int u32;
u32 native_utility_child_arm7_main_027e94c8(u32 address) {
    u32 value;
    if (address & 1) value = (u8)((int)*(u16 *)(address - 1) >> 8);
    else value = (u8)*(u16 *)address;
    return (u8)value;
}
