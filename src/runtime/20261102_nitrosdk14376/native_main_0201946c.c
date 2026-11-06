typedef unsigned long u32;
        typedef int BOOL;
    typedef u32 OSIntrMode;
    extern OSIntrMode native_fn_02007ff4(void);
    extern OSIntrMode native_fn_02008008(OSIntrMode state);
void native_fn_02007748(u32 setMask, u32 flags);
BOOL native_fn_020191d4(void);
void native_main_0201946c(BOOL enable);
extern BOOL native_data_main_020ec3b8;
BOOL native_fn_020191d4 (void);
void native_main_0201946c (BOOL enable)
{
	OSIntrMode bak_cpsr = native_fn_02007ff4();
	native_data_main_020ec3b8 = enable;
	if (!native_fn_020191d4()) {
		u32 acc = (u32)(enable ? (1 << 12) : (5 << 12) );
		(void)native_fn_02007748((0xf << 12) , acc);
	}
	(void)native_fn_02008008(bak_cpsr);
}
