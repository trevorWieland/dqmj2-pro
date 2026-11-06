typedef unsigned int u32;
typedef unsigned short u16;
typedef signed int s32;

u32 native_main_0200427c(void) {
    u32 control = *(volatile u32 *)0x04001000;
    u16 configuration = *(volatile u16 *)0x0400100E;
    s32 mode = (s32)(control & 7);
    if (mode < 3 || (mode < 6 && !(configuration & 0x80))) {
        return (((u32)(configuration & 0x3C) >> 2) << 14) + 0x06200000;
    }
    return 0;
}
