typedef enum {
	PM_LED_PATTERN_NONE          = 0,
	PM_LED_PATTERN_ON            = 1,
	PM_LED_PATTERN_BLINK_LOW     = 2,
	PM_LED_PATTERN_BLINK_HIGH    = 3,
	PM_LED_PATTERN_BLINK1        = 4,
	PM_LED_PATTERN_BLINK2        = 5,
	PM_LED_PATTERN_BLINK3        = 6,
	PM_LED_PATTERN_BLINK4        = 7,
	PM_LED_PATTERN_BLINK5        = 8,
	PM_LED_PATTERN_BLINK6        = 9,
	PM_LED_PATTERN_BLINK8        = 10,
	PM_LED_PATTERN_BLINK10       = 11,
	PM_LED_PATTERN_PATTERN1      = 12,
	PM_LED_PATTERN_PATTERN2      = 13,
	PM_LED_PATTERN_PATTERN3      = 14,
	PM_LED_PATTERN_WIRELESS      = 15
} PMLEDPattern;

void native_utility_child_arm7_arm_027e2eec(PMLEDPattern pattern);

extern const u16 (*ctrdgi_fl_maxtime);

typedef	struct {
	u16		code;
	u16		length;
} WlCmdHeader;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlDevShutdownCfm;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				buf[2];
} WlCmdCfm;

typedef struct WMSPWork {
    OSMessageQueue toWLmsgQ;
    OSMessage toWLmsg[2 ];
    OSMessageQueue fromWLmsgQ;
    OSMessage fromWLmsg[4 ];
    OSMessageQueue confirmQ;
    OSMessage confirm[4 ];
    OSMessageQueue requestQ;
    OSMessage request[32 ];
    u32 requestStack[4096 / sizeof(u32)];
    u32 indicateStack[1024 / sizeof(u32)];
    OSMutex fifoExclusive;
    u32 dmaNo;
    OSArenaId arenaId;
    OSHeapHandle heapHandle;
    WMArm7Buf *wm7buf;
    WMStatus *status;
    u8 rssiHistory[32 ];
    u32 rssiIndex;
    u32 indPrio_high;
    u32 wlPrio_high;
    u32 reqPrio_high;
    u32 indPrio_low;
    u32 wlPrio_low;
    u32 reqPrio_low;
} WMSPWork;

extern WMSPWork native_utility_child_arm7_data_027f84f0;

void native_utility_child_arm7_arm_038057c8(void *ptr);

void *native_utility_child_arm7_arm_0380576c(void);

void native_utility_child_arm7_main_027e3378(OSMessage msg);

WlDevShutdownCfm *native_utility_child_arm7_arm_027e2268(u16 *buf);

static inline WMStatus *WMSP_GetStatusStructure(void)
{
    return native_utility_child_arm7_data_027f84f0.status;
}

static void native_utility_child_arm7_arm_027e333c(u16 wlCommand, u16 wlResult);
