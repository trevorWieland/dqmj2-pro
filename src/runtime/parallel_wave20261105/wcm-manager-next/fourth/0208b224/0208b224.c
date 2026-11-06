#include "context.h"
WMBssDesc * native_main_0208b224 (s32 index)
{
    OSIntrMode e = native_fn_02007ff4();
    WCMWork * w = native_fn_0208a31c();
    WMBssDesc * bd = NULL;
    WCMApList * p;
    if (w == NULL) {
        WCMi_Warning(aplistWarningText_NotInit);
        (void)native_fn_02008008(e);
        return NULL;
    }
    p = native_fn_0208b3a4((u32) index);
    if (p == NULL) {
        WCMi_Warning(aplistWarningText_NoIndexData, index);
        (void)native_fn_02008008(e);
        return NULL;
    }
    bd = (WMBssDesc *) (p->data);
    (void)native_fn_02008008(e);
    return bd;
}
