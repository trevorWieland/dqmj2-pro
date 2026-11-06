typedef unsigned short int u16;
typedef unsigned long u32;
    typedef u32 OSIntrMode;
    extern OSIntrMode native_fn_02007ff4(void);
    extern OSIntrMode native_fn_02008008(OSIntrMode state);
void native_fn_02005c64(u32 dmaNo, void (*callback)(void *), void * arg);
typedef void (*MIDmaCallback) (void *);
void native_main_020085b8(u32 dmaNo, void * dest, u32 data, u32 size, MIDmaCallback callback, void * arg);
void native_fn_02008714(u32 dmaNo);
extern const u16 (*ctrdgi_fl_maxtime);
typedef union {
    u32 b32;
    u16 b16;
} MIiDmaClearSrc;
    void native_fn_01ff84f8(u32 dmaNo, u32 src, u32 dest, u32 ctrl);
static inline void MIi_DmaSetParams_src32 (u32 dmaNo, u32 data, u32 dest, u32 ctrl)
{
    OSIntrMode enabled = native_fn_02007ff4();
    MIiDmaClearSrc * srcp = (MIiDmaClearSrc *) ((u32)(0x04000000 + 0x0e0) + dmaNo * 4);
    srcp->b32 = data;
    native_fn_01ff84f8(dmaNo, (u32)srcp, dest, ctrl);
    (void)native_fn_02008008(enabled);
}
extern void native_fn_02005c64(u32 dmaNo, MIDmaCallback callback, void * arg);
static inline void MIi_CallCallback (MIDmaCallback callback, void * arg)
{
    if (callback) {
        (callback) (arg);
    }
}
    void native_fn_01ff84f8 (u32 dmaNo, u32 src, u32 dest, u32 ctrl);
void native_main_020085b8 (u32 dmaNo, void * dest, u32 data, u32 size, MIDmaCallback callback, void * arg)
{
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0); ;
    ((void) 0) ;
    ((void)0) ;
    if (size == 0) {
        MIi_CallCallback(callback, arg);
    } else {
        native_fn_02008714(dmaNo);
        if (callback) {
            native_fn_02005c64(dmaNo, callback, arg);
            MIi_DmaSetParams_src32(dmaNo, data, (u32)dest, ((((1UL << 31) | (0UL << 27) | (1UL << 26)) | (2UL << 23) | (0UL << 21) | (((size)) / 4)) | (1UL << 30)) );
        } else {
            MIi_DmaSetParams_src32(dmaNo, data, (u32)dest, (((1UL << 31) | (0UL << 27) | (1UL << 26)) | (2UL << 23) | (0UL << 21) | ((size) / 4)) );
        }
    }
}
void native_fn_02008714 (u32 dmaNo);
