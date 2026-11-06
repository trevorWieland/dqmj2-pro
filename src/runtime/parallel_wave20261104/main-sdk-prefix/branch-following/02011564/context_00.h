typedef unsigned long u32;
typedef signed long s32;
typedef int BOOL;
void native_fn_020004fc(s32 count);
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
int native_fn_0200a440(int fifotag, u32 data, BOOL err);
void native_main_02011564(u32 data, u32 wait);
