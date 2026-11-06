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

s32 native_utility_child_arm9_thumb_0200d6c4(const RTCDate * date);

s32 native_utility_child_arm9_thumb_0200d6b0(const RTCTime * time);

s64 native_utility_child_arm9_main_0200d660(const RTCDate * date, const RTCTime * time);

s32 native_utility_child_arm9_thumb_0200d6c4 (const RTCDate * date);

s32 native_utility_child_arm9_thumb_0200d6b0 (const RTCTime * time);
