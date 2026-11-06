typedef unsigned long u32;

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

RTCWeek native_utility_child_arm9_main_0200d5ec(RTCDate * date);
