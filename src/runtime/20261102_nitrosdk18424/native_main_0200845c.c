typedef unsigned short int u16;
typedef unsigned long u32;
typedef volatile u32 vu32;
    typedef u32 OSIntrMode;
    extern OSIntrMode native_fn_02007ff4(void);
    extern OSIntrMode native_fn_02008008(OSIntrMode state);
void native_main_0200845c(u32 dmaNo, void * dest, u32 data, u32 size);
extern const u16 (*ctrdgi_fl_maxtime);
typedef union {
    u32 b32;
    u16 b16;
} MIiDmaClearSrc;
    void native_fn_01ff851c(u32 dmaNo, u32 src, u32 dest, u32 ctrl);
static inline void MIi_DmaSetParams_wait_src32 (u32 dmaNo, u32 data, u32 dest, u32 ctrl)
{
    OSIntrMode enabled = native_fn_02007ff4();
    MIiDmaClearSrc * srcp = (MIiDmaClearSrc *) ((u32)(0x04000000 + 0x0e0) + dmaNo * 4);
    srcp->b32 = data;
    native_fn_01ff851c(dmaNo, (u32)srcp, dest, ctrl);
    (void)native_fn_02008008(enabled);
}
    void native_fn_01ff851c (u32 dmaNo, u32 src, u32 dest, u32 ctrl);
void native_main_0200845c (u32 dmaNo, void * dest, u32 data, u32 size)
{
    vu32 * dmaCntp;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0); ;
    ((void) 0) ;
    ((void)0) ;
    if (size == 0) {
        return;
    }
    do { dmaCntp = &((vu32 *)(0x04000000 + 0x0b0))[ dmaNo * 3 + 2]; ((void) 0); while ( *dmaCntp & 0x80000000 ) {} } while (0) ;
    MIi_DmaSetParams_wait_src32(dmaNo, data, (u32)dest, (((1UL << 31) | (0UL << 27) | (1UL << 26)) | (2UL << 23) | (0UL << 21) | ((size) / 4)) );
    do { while ( *dmaCntp & 0x80000000 ) {} } while (0) ;
}
