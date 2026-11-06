typedef unsigned short int u16;
typedef unsigned long u32;
typedef volatile u32 vu32;
        typedef int BOOL;
    typedef u32 OSIntrMode;
    extern OSIntrMode native_utility_child_arm9_arm_0200a64c(void);
    extern OSIntrMode native_utility_child_arm9_arm_0200a660(OSIntrMode state);
typedef enum {
	PXI_FIFO_TAG_EX = 0,
	PXI_FIFO_TAG_USER_0,
	PXI_FIFO_TAG_USER_1,
	PXI_FIFO_TAG_SYSTEM,
	PXI_FIFO_TAG_NVRAM,
	PXI_FIFO_TAG_RTC,
	PXI_FIFO_TAG_TOUCHPANEL,
	PXI_FIFO_TAG_SOUND,
	PXI_FIFO_TAG_PM,
	PXI_FIFO_TAG_MIC,
	PXI_FIFO_TAG_WM,
	PXI_FIFO_TAG_FS,
	PXI_FIFO_TAG_OS,
	PXI_FIFO_TAG_CTRDG,
	PXI_FIFO_TAG_CARD,
	PXI_FIFO_TAG_WVR,
	PXI_FIFO_TAG_CTRDG_Ex,
	PXI_FIFO_TAG_CTRDG_PHI,
	PXI_MAX_FIFO_TAG = 32
} PXIFifoTag;
extern const u16 (*ctrdgi_fl_maxtime);
void native_utility_child_arm9_main_0200f7c0(u32 id);
static void native_utility_child_arm9_thumb_0200f86c(PXIFifoTag tag, u32 data, BOOL err);
void native_utility_child_arm9_thumb_0200f86c (PXIFifoTag tag, u32 data, BOOL err);
void native_utility_child_arm9_main_0200f7c0 (u32 id)
{
	vu32 iplCardID = *(vu32 *)((*(u16 *)0x027ffc10 ==
	                            0) ? (0x02000000 + 0x007ff800) : (0x02000000 + 0x007ffc00) );
	if (id != (u32)iplCardID) {
		OSIntrMode bak_cpsr = native_utility_child_arm9_arm_0200a64c();
		native_utility_child_arm9_thumb_0200f86c(PXI_FIFO_TAG_CARD, 0x0011 , 0 );
		(void)native_utility_child_arm9_arm_0200a660(bak_cpsr);
	}
}
