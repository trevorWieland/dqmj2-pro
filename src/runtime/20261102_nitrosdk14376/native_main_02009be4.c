typedef unsigned long u32;
typedef volatile u32 vu32;
        typedef int BOOL;
    typedef u32 OSIntrMode;
    extern OSIntrMode native_fn_02007ff4(void);
    extern OSIntrMode native_fn_02008008(OSIntrMode state);
BOOL native_fn_02006ddc(void);
    BOOL native_main_02009be4(void);
    BOOL native_main_02009be4 (void)
    {
        OSIntrMode prev_mode;
        u32 res;
        if (!native_fn_02006ddc())
            return 1 ;
        prev_mode = native_fn_02007ff4();
        *(vu32 *)0x4fff200 = 0x10;
        res = *(vu32 *)0x4fff200;
        (void)native_fn_02008008(prev_mode);
        return res ? 1 : 0 ;
    }
