#include "context000.h"

#include "context001.h"

void WMSP_RequestThread(void *arg)
{
    WMSPWork *p = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    OSMessage msg;
    u16 apiid;
    while (1 ) {
        (void)OS_ReceiveMessage(&(p->requestQ), &msg, 1 );
        if (msg == 0) {
            OS_ExitThread();
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
            (WmspRequestFuncTable[apiid])(msg);
            status->apiBusy = 0 ;
        } else {
        }
        *((u16 *)msg) = (u16)(apiid | 0x8000 );
    }
}

#include "context002.h"
