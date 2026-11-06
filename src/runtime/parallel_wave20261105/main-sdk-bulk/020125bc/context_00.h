typedef unsigned short int u16;
typedef unsigned long u32;
u16 native_main_020125bc(void);
typedef enum RTCResult {
	RTC_RESULT_SUCCESS = 0,
	RTC_RESULT_BUSY,
	RTC_RESULT_ILLEGAL_PARAMETER,
	RTC_RESULT_SEND_ERROR,
	RTC_RESULT_INVALID_COMMAND,
	RTC_RESULT_ILLEGAL_STATUS,
	RTC_RESULT_FATAL_ERROR,
	RTC_RESULT_MAX
} RTCResult;
typedef struct RTCTime {
	u32 hour;
	u32 minute;
	u32 second;
} RTCTime;
void native_fn_0200f304(void);
RTCResult native_fn_0200f48c(RTCTime * time);
extern const u16 (*ctrdgi_fl_maxtime);
typedef struct {
u32 field_0000;
} NativeStorage_020dce84;
extern NativeStorage_020dce84 native_data_main_020dce84;
