typedef unsigned short u16;
typedef unsigned int u32;

extern u16 native_data_027fffa8[];

u32 native_ov006_021f79ac(void) {
    if (((native_data_027fffa8[0] & 0x8000) >> 15) != 0) return 1;
    return 0;
}
