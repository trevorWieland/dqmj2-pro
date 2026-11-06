#include "context.h"
void native_main_0208b154 (void)
{
    OSIntrMode e = native_fn_02007ff4();
    WCMWork * w = native_fn_0208a31c();
    if (w == NULL) {
        WCMi_Warning(aplistWarningText_NotInit);
        (void)native_fn_02008008(e);
        return;
    }
    if ((w->config.pbdbuffer != NULL) && (w->config.nbdbuffer > 0)) {
        MI_CpuClear8(w->config.pbdbuffer, (u32) (w->config.nbdbuffer));
    }
    (void)native_fn_02008008(e);
}
