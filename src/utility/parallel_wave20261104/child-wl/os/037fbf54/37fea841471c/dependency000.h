typedef unsigned short int u16;

typedef unsigned long u32;

typedef signed long s32;

typedef int BOOL;

typedef u32 OSIntrMode;

extern OSIntrMode native_utility_child_arm7_arm_037fe41c(void);

extern OSIntrMode native_utility_child_arm7_arm_037fe430(OSIntrMode state);

extern OSIntrMode native_utility_child_arm7_arm_037fe448(void);

extern OSIntrMode native_utility_child_arm7_arm_037fe45c(OSIntrMode state);

typedef volatile struct OSLockWord {
	u32 lockFlag;
	u16 ownerID;
	u16 extension;
} OSLockWord;

u32 native_utility_child_arm7_arm_037fe944(u32 setData, volatile u32 * destp);

extern const u16 (*ctrdgi_fl_maxtime);

s32 native_utility_child_arm7_wram_037fbf54(u16 lockID, OSLockWord * lockp, void (*ctrlFuncp)(void), BOOL disableFIQ);
