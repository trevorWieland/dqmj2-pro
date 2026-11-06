#include "context_00.h"
void native_main_0200fe50 (RTCDate * date, RTCTime * time, s64 sec)
{
    if (sec < 0) {
        sec = 0;
    } else if (sec > 3155759999)   {
        sec = 3155759999;
    }
    native_fn_0200fdd0(time, (s32)(sec % 86400));
    native_fn_0200fcd0(date, (s32)(sec / 86400));
}
