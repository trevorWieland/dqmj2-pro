typedef unsigned short u16;
typedef unsigned int u32;
u32 native_utility_child_arm7_main_027e94e8(u32 address, u32 value) {
    if (address & 1) *(u16 *)(address - 1) = (*(u16 *)(address - 1) & 255) | (value << 8);
    else *(u16 *)address = (*(u16 *)address & 0xFF00) | (value & 255);
    return address;
}
