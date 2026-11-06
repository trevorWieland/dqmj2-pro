#include "poll.h"
s32 native_main_020907f4(PollEntry *entries,u32 count,u64 timeout)
{
    PollEntry *entry;
    s32 enabled;
    s64 time;
    s32 index,good;
    s32 status,mask;
    enabled=timeout!=(u64)-1;
    time=(s64)timeout;
    for(;;){
        entry=entries;
        good=0;
        for(index=0;index<count;index++){
            mask=entry->events|0xe0;
            status=native_fn_02090138(entry->fd)&mask;
            if(status)good++;
            entry->revents=(s16)status;
            entry++;
        }
        if(good>0 || (enabled && time<=0))break;
        native_fn_02006b7c(1);
        time-=(s64)(((u64)33513982)/(64*1000));
    }
    return good;
}
