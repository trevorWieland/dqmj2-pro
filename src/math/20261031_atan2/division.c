typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef unsigned long long u64;
extern u32 native_fn_02002458(u32 numerator, s32 denominator);
extern u32 native_fn_020023c4(void);

u32 native_main_0200235c(u32 numerator, s32 denominator) {
    native_fn_02002458(numerator, denominator);
    return native_fn_020023c4();
}

u32 native_main_020023c4(void) {
    volatile u16 *control = (volatile u16 *)0x04000280;
    u64 quotient;
    while (*control & 0x8000) {
    }
    quotient = *(u64 *)0x040002A0;
    return (u32)((quotient + 0x80000) >> 20);
}
