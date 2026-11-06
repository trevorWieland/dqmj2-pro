#include "dependency000.h"

s64 native_utility_child_arm9_main_0200d660 (const RTCDate * date, const RTCTime * time)
{
    s32 day, sec;
    day = native_utility_child_arm9_thumb_0200d6c4(date);
    if (day == -1) {
        return -1;
    }
    sec = native_utility_child_arm9_thumb_0200d6b0(time);
    if (sec == -1) {
        return -1;
    }
    return ((s64)day) * (60 * 60 * 24) + sec;
}
