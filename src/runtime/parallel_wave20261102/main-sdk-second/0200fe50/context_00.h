typedef unsigned long u32;
typedef signed long s32;
typedef signed long long int s64;
typedef enum RTCWeek {
	RTC_WEEK_SUNDAY = 0,
	RTC_WEEK_MONDAY,
	RTC_WEEK_TUESDAY,
	RTC_WEEK_WEDNESDAY,
	RTC_WEEK_THURSDAY,
	RTC_WEEK_FRIDAY,
	RTC_WEEK_SATURDAY,
	RTC_WEEK_MAX
} RTCWeek;
typedef struct RTCDate {
	u32 year;
	u32 month;
	u32 day;
	RTCWeek week;
} RTCDate;
typedef struct RTCTime {
	u32 hour;
	u32 minute;
	u32 second;
} RTCTime;
void native_fn_0200fcd0(RTCDate * date, s32 day);
void native_fn_0200fdd0(RTCTime * time, s32 sec);
void native_main_0200fe50(RTCDate * date, RTCTime * time, s64 sec);
void native_fn_0200fcd0 (RTCDate * date, s32 day);
void native_fn_0200fdd0 (RTCTime * time, s32 sec);
