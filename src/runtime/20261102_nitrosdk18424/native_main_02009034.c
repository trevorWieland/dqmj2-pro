typedef unsigned long u32;
typedef volatile u32 vu32;
void native_main_02009034(u32 dmaNo, const void * src, void * dest, u32 size);
    void native_fn_01ff8448(u32 dmaNo, u32 src, u32 dest, u32 ctrl);
    void native_fn_02008820(u32 dmaNo, u32 dmaType);
void native_fn_020088a4(u32 dmaNo, u32 src, u32 size, u32 dir);
void native_main_02009034 (u32 dmaNo, const void * src, void * dest, u32 size)
{
    vu32 * dmaCntp;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void)0) ;
    (void)size;
    native_fn_02008820(dmaNo, (u32)(~0) );
    native_fn_020088a4(dmaNo, (u32)src, size, (2UL << 23) );
    if (size == 0) {
        return;
    }
    do { dmaCntp = &((vu32 *)(0x04000000 + 0x0b0))[ dmaNo * 3 + 2]; ((void) 0); while ( *dmaCntp & 0x80000000 ) {} } while (0) ;
    native_fn_01ff8448(dmaNo, (u32)src, (u32)dest, (u32)(((1UL << 31) | (5UL << 27) | (2UL << 23) | (0UL << 21) | (1UL << 26) | ((4) / 4)) | (1UL << 25) ));
}
