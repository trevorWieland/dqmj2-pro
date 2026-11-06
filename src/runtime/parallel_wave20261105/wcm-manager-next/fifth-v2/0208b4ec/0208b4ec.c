#include "context.h"
u8 * native_main_0208b4ec (void)
{
    u8 * mac = NULL;
    WCMWork * w = native_fn_0208a31c();
    OSIntrMode e = native_fn_02007ff4();
    if (w != NULL) {
        if ((w->phase == WCM_PHASE_DCF) && (w->resetting == WCM_RESETTING_OFF)) {
            mac = w->bssDesc.bssid;
        }
    }
    (void)native_fn_02008008(e);
    return mac;
}
