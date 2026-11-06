typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed long s32;
typedef int BOOL;
void native_fn_020004fc(s32 count);
typedef volatile struct OSLockWord {
	u32 lockFlag;
	u16 ownerID;
	u16 extension;
} OSLockWord;
extern const u16 (*ctrdgi_fl_maxtime);
s32 native_main_02005eac(u16 lockID, OSLockWord * lockp, void (*ctrlFuncp)(void), BOOL disableFiq);
s32 native_fn_02005f8c(u16 lockID, OSLockWord * lockp, void (*ctrlFuncp)(void), BOOL disableFIQ);
static void OSi_WaitByLoop(void);
s32 native_fn_02005f8c (u16 lockID, OSLockWord * lockp, void (*ctrlFuncp)(void), BOOL disableFIQ);
static inline void OSi_WaitByLoop (void)
{
    native_fn_020004fc(0x1000 / 4);
}
