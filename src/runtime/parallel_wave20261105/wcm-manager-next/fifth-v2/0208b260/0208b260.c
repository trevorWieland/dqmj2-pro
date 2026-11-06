#include "context.h"
void native_main_0208b260 (WMBssDesc * bssDesc, u16 linkLevel)
{
    WCMWork * w = native_fn_0208a31c();
    WCMApList * aplist;
    if (w == NULL) {
        return;
    }
    if (w->apListLock != WCM_APLIST_UNLOCK) {
        return;
    }
    if (bssDesc->gameInfoLength != 0) {
        return;
    }
    {
        aplist = native_fn_0208b35c(bssDesc->bssid);
        if (aplist == NULL) {
            aplist = native_fn_0208b2c0();
        }
        if ((aplist == NULL) && (w->config.nbdmode == WCM_APLIST_MODE_EXCHANGE)) {
            aplist = native_fn_0208b338();
        }
    }
    if (aplist != NULL) {
        aplist->linkLevel = linkLevel;
        native_fn_02008ca4(bssDesc, aplist->data, WCM_APLIST_SIZE);
        native_fn_0208b3d8(aplist);
    }
}
