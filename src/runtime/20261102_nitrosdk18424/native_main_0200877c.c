typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed long s32;
typedef volatile u16 vu16;
typedef volatile u32 vu32;
    typedef u32 OSIntrMode;
    extern OSIntrMode native_fn_02007ff4(void);
    extern OSIntrMode native_fn_02008008(OSIntrMode state);
void native_main_0200877c(u32 dmaNo);
extern const u16 (*ctrdgi_fl_maxtime);
void native_main_0200877c (u32 dmaNo)
{
    OSIntrMode enabled = native_fn_02007ff4();
    vu16 * dmaCntp = &((vu16 *)(0x04000000 + 0x0b0) )[dmaNo * 6 + 5];
    ((void) 0) ;
    *dmaCntp &= ~(((0x38000000) | (1UL << 25) ) >> 16);
    *dmaCntp &= ~((1UL << 31) >> 16);
    {
        s32 dummy = dmaCntp[0];
    }
    {
        s32 dummy = dmaCntp[0];
    }
    if (dmaNo == 0 ) {
        vu32 * p = (vu32 *)((u32)(0x04000000 + 0x0b0) + dmaNo * 12);
        *p = (vu32)0 ;
        *(p + 1) = (vu32)0 ;
        *(p + 2) = (vu32)((1UL << 31) | (2UL << 23) | (2UL << 21) | (0UL << 26) | 1) ;
    }
    (void)native_fn_02008008(enabled);
}
