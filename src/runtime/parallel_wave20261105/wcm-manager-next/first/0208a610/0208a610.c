#include "context.h"
void native_main_0208a610(void)
{
    OSIntrMode  e = native_fn_02007ff4();
    native_fn_02007e10(&(native_data_021cfcb4->keepAliveAlarm));
    if (native_data_021cfcb4->phase == WCM_PHASE_DCF)
    {
        native_fn_02007da4(&(native_data_021cfcb4->keepAliveAlarm), OS_SecondsToTicks(WCM_KEEP_ALIVE_SPAN), native_fn_0208a660, NULL);
    }
    (void)native_fn_02008008(e);
}
