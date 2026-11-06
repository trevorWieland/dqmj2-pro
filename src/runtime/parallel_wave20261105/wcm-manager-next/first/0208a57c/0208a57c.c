#include "context.h"
void native_main_0208a57c(s16 notify, s16 result, void* para0, void* para1, s32 para2)
{
    if (native_data_021cfcb4->notify)
    {
        WCMNotice   notice;
        notice.notify = notify;
        notice.result = result;
        notice.parameter[0].p = para0;
        notice.parameter[1].p = para1;
        notice.parameter[2].n = para2;
        native_data_021cfcb4->notify(&notice);
    }
}
