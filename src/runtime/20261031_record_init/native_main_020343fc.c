typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
extern u32 native_data_020dd5f8;

u32 native_main_020343fc(u8 *destination, u32 word, const u8 *source) {
    u32 index = 0;
    *(u32 *)(destination + 12) = native_data_020dd5f8;
    destination[25] = source[23];
    *(u32 *)(destination + 8) = word;
    if (index >= destination[25]) {
        return (u32)destination;
    }
    do {
        *(u16 *)(destination + 26 + index * 2) = (u16)(index | 0x100);
        index++;
    } while (index < destination[25]);
    return (u32)destination;
}
