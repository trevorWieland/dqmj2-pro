typedef unsigned long u32;
typedef signed long s32;
u32 native_main_0200fac8(u32 bcd);
u32 native_main_0200fac8 (u32 bcd)
{
    u32 hex = 0;
    s32 i;
    s32 w;
    for (i = 0; i < 8; i++) {
        if (((bcd >> (i * 4)) & 0x0000000f) >= 0x0a) {
            return hex;
        }
    }
    for (i = 0, w = 1; i < 8; i++, w *= 10) {
        hex += (((bcd >> (i * 4)) & 0x0000000f) * w);
    }
    return hex;
}
