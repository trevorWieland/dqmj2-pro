#include "context_00.h"
WMErrCode native_main_02012774 (void * wmSysBuf, WMCallbackFunc callback, u16 dmaNo, BOOL blink)
{
    u32 miscFlags = 0x0001 ;
    if (!blink) {
        miscFlags |= 0x0002 ;
    }
    return native_fn_0201278c(wmSysBuf, callback, dmaNo, miscFlags);
}
