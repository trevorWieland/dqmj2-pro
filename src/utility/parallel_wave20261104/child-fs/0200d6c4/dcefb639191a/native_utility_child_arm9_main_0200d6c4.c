#include "dependency000.h"

s32 native_utility_child_arm9_main_0200d6c4 (const RTCDate * date)
{
    s32 dayNum;
    if (date->year >= 100
        || (date->month < 1) || (date->month > 12)
        || (date->day < 1) || (date->day > 31)
        || (date->week >= RTC_WEEK_MAX) || (date->month < 1) || (date->month > 12)) {
        return -1;
    }
    dayNum = (s32)(date->day - 1);
    dayNum += native_utility_child_arm9_data_020225e4[date->month - 1];
    if ((date->month >= 3) && RTCi_IsLeapYear(date->year)) {
        dayNum++;
    }
    dayNum += date->year * 365;
    dayNum += (date->year + 3) / 4;
    return dayNum;
}
