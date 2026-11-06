#include "context.h"
void native_main_0208b498 (void)
{
    volatile WCMWork * w = native_fn_0208a31c();
    if (w == NULL) {
        return;
    }
    if ((w->phase != WCM_PHASE_DCF) || (w->resetting == WCM_RESETTING_ON)) {
        return;
    }
    if (FALSE == native_fn_0208b6e0(&(native_data_021cfcb8.sendMutex))) {
        return;
    }
    if (WM_ERRCODE_OPERATING != native_fn_02013328(native_fn_0208b6d0, (const u8 *)w->bssDesc.bssid, (const u16 *)(w->sendBuf), 0)) {
        native_fn_0208b70c(&(native_data_021cfcb8.sendMutex));
    }
}
