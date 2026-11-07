typedef unsigned short int u16;

typedef unsigned long u32;

typedef struct RTCRawStatus1 {
	u16 reset :1;
	u16 format :1;
	u16 dummy0 :2;
	u16 intr1 :1;
	u16 intr2 :1;
	u16 bld :1;
	u16 poc :1;
	u16 dummy1 :8;
} RTCRawStatus1;

typedef struct RTCRawStatus2 {
	u16 intr_mode :4;
	u16 dummy0 :2;
	u16 intr2_mode :1;
	u16 test :1;
	u16 dummy1 :8;
} RTCRawStatus2;

typedef enum RTCPxiResult {
	RTC_PXI_RESULT_SUCCESS = 0,
	RTC_PXI_RESULT_INVALID_COMMAND,
	RTC_PXI_RESULT_ILLEGAL_STATUS,
	RTC_PXI_RESULT_BUSY,
	RTC_PXI_RESULT_FATAL_ERROR,
	RTC_PXI_RESULT_MAX
} RTCPxiResult;

void native_host_arm7_arm_027f6b10(RTCRawStatus1 *stat);

void native_host_arm7_arm_027f6b74(RTCRawStatus2 *stat);

void native_host_arm7_arm_027f6ba0(const RTCRawStatus2 *stat);

extern const u16 (*ctrdgi_fl_maxtime);

extern void native_host_arm7_arm_027f6074(u16 command, RTCPxiResult result);

void native_host_arm7_main_027f6538(void);

void native_host_arm7_arm_027f6074(u16 command, RTCPxiResult result);
