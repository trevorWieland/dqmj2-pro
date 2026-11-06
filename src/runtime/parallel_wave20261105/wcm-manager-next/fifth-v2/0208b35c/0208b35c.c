#include "context.h"
WCMApList * native_main_0208b35c (u8 * bssid)
{
    WCMWork * w = native_fn_0208a31c();
    WCMApListHeader * pHeader = (WCMApListHeader *) (w->config.pbdbuffer);
    WCMApList * p = NULL;
    if (bssid == NULL) {
        return NULL;
    }
    if ((pHeader != NULL) && (w->config.nbdbuffer > sizeof(WCMApListHeader))) {
        p = pHeader->head;
        while (p) {
            if (native_fn_0208b72c(((WMBssDesc *) (p->data))->bssid, bssid)) {
                break;
            }
            p = p->next;
        }
    }
    return p;
}
