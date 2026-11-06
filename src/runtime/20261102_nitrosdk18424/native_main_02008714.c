typedef unsigned long u32;
typedef volatile u32 vu32;
    typedef u32 OSIntrMode;
    extern OSIntrMode native_fn_02007ff4(void);
    extern OSIntrMode native_fn_02008008(OSIntrMode state);
void native_main_02008714(u32 dmaNo);
void native_main_02008714 (u32 dmaNo)
{
    OSIntrMode enabled = native_fn_02007ff4();
    vu32 * dmaCntp = &((vu32 *)(0x04000000 + 0x0b0) )[dmaNo * 3 + 2];
    ((void) 0) ;
    while (*dmaCntp & 0x80000000 ) {
    }
    if (dmaNo == 0 ) {
        vu32 * p = (vu32 *)((u32)(0x04000000 + 0x0b0) + dmaNo * 12);
        *p = (vu32)0 ;
        *(p + 1) = (vu32)0 ;
        *(p + 2) = (vu32)((1UL << 31) | (2UL << 23) | (2UL << 21) | (0UL << 26) | 1) ;
    }
    (void)native_fn_02008008(enabled);
}
