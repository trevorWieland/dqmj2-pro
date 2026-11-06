typedef unsigned long u32;
typedef signed long s32;
        typedef int BOOL;
void native_utility_child_arm9_thumb_02000804(s32 count);
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
typedef enum {
	PXI_FIFO_SUCCESS              = 0,
	PXI_FIFO_FAIL_SEND_ERR        = -1,
	PXI_FIFO_FAIL_SEND_FULL       = -2,
	PXI_FIFO_FAIL_RECV_ERR        = -3,
	PXI_FIFO_FAIL_RECV_EMPTY      = -4,
	PXI_FIFO_NO_CALLBACK_ENTRY    = -5
} PXIFifoStatus;
int native_utility_child_arm9_thumb_0200f9b4(int fifotag, u32 data, BOOL err);
void native_utility_child_arm9_main_0200f788(u32 data, u32 wait);
void native_utility_child_arm9_main_0200f788 (u32 data, u32 wait)
{
	while (native_utility_child_arm9_thumb_0200f9b4(PXI_FIFO_TAG_CARD, data, 0 ) != PXI_FIFO_SUCCESS) {
		native_utility_child_arm9_thumb_02000804((s32)wait);
	}
}
