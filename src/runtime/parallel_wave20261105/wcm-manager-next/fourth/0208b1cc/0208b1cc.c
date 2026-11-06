#include "context.h"
s32 native_main_0208b1cc (s32 lock)
{
    OSIntrMode e = native_fn_02007ff4();
    WCMWork * w = native_fn_0208a31c();
    if (w == NULL) {
        WCMi_Warning(aplistWarningText_NotInit);
        (void)native_fn_02008008(e);
        return 0;
    }
    if (lock != WCM_APLIST_UNLOCK) {
        lock = (w->apListLock ? WCM_APLIST_LOCK : WCM_APLIST_UNLOCK);
        w->apListLock = WCM_APLIST_LOCK;
    } else {
        lock = (w->apListLock ? WCM_APLIST_LOCK : WCM_APLIST_UNLOCK);
        w->apListLock = WCM_APLIST_UNLOCK;
    }
    (void)native_fn_02008008(e);
    return lock;
}
