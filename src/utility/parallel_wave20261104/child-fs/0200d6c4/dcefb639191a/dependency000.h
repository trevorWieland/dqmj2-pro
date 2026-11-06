typedef unsigned long u32;

typedef signed long s32;

typedef int BOOL;

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

s32 native_utility_child_arm9_main_0200d6c4(const RTCDate * date);

extern s32 native_utility_child_arm9_data_020225e4[12];

static inline BOOL RTCi_IsLeapYear (u32 year)
{
    return !((year & 0x03));
}
