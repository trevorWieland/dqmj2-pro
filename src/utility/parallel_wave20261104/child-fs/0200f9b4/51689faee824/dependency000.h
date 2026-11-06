typedef unsigned short int u16;

typedef unsigned long u32;

typedef volatile u16 vu16;

typedef volatile u32 vu32;

typedef vu16 REGType16v;

typedef vu32 REGType32v;

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

typedef enum {
	PXI_FIFO_SUCCESS              = 0,
	PXI_FIFO_FAIL_SEND_ERR        = -1,
	PXI_FIFO_FAIL_SEND_FULL       = -2,
	PXI_FIFO_FAIL_RECV_ERR        = -3,
	PXI_FIFO_FAIL_RECV_EMPTY      = -4,
	PXI_FIFO_NO_CALLBACK_ENTRY    = -5
} PXIFifoStatus;

typedef union {
	struct {
		u32 tag : 5 ;
		u32 err : 1 ;
		u32 data : 26 ;
	} e;
	u32 raw;
} PXIFifoMessage;

int native_utility_child_arm9_main_0200f9b4(int fifotag, u32 data, BOOL err);

extern const u16 (*ctrdgi_fl_maxtime);

static inline PXIFifoStatus PXIi_SetToFifo(u32 data);
