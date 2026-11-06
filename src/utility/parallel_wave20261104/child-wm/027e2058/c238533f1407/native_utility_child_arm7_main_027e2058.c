#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e2058(void *arg)
{
    WMSPWork *p = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    OSMessage msg;
    u16 apiid;
    while (1 ) {
        (void)native_utility_child_arm7_arm_037fcc2c(&(p->requestQ), &msg, 1 );
        if (msg == 0) {
            native_utility_child_arm7_arm_037fc5c0();
            return;
        }
        apiid = *((u16 *)msg);
        if (apiid & 0x8000 ) {
            apiid &= ~(0x8000 );
        }
        if (apiid < WM_APIID_ASYNC_KIND_MAX) {
            ((void)0) ;
            status->apiBusy = 1 ;
            status->BusyApiid = apiid;
            (native_utility_child_arm7_data_027f7df8[apiid])(msg);
            status->apiBusy = 0 ;
        } else {
        }
        *((u16 *)msg) = (u16)(apiid | 0x8000 );
    }
}
#include "dependency002.h"
