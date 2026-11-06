#include "context.h"
u8 * native_main_0208b524 (u16 * length)
{
    u8 * essid = NULL;
    u16 len = 0;
    WCMWork * w = native_fn_0208a31c();
    OSIntrMode e = native_fn_02007ff4();
    if (w != NULL) {
        if ((w->phase == WCM_PHASE_DCF) && (w->resetting == WCM_RESETTING_OFF)) {
            essid = &(w->bssDesc.ssid[0]);
            len = w->bssDesc.ssidLength;
        }
    }
    (void)native_fn_02008008(e);
    if (length != NULL) {
        *length = len;
    }
    return essid;
}
