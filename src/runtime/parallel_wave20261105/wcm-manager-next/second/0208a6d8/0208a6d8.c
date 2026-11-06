#include "context.h"
void native_main_0208a6d8(void* arg)
{
    WMIndCallback*  cb = (WMIndCallback*)arg;
    if (cb->errcode == WM_ERRCODE_FIFO_ERROR)
    {
        if ((cb->state == WM_STATECODE_FIFO_ERROR) && (cb->reason == WM_APIID_AUTO_DISCONNECT))
        {
            switch (native_data_021cfcb4->phase)
            {
            case WCM_PHASE_IDLE_TO_DCF:
                native_fn_0208a5ac(WCM_PHASE_IRREGULAR);
                break;
            case WCM_PHASE_DCF:
            case WCM_PHASE_IRREGULAR:
                native_fn_0208a698();
                break;
            case WCM_PHASE_DCF_TO_IDLE:
                native_fn_0208a5ac(WCM_PHASE_IRREGULAR);
                break;
            }
        }
    }
}
