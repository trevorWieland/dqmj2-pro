#include "context000.h"

u32 *WMSP_GetInternalRequestBuf(void)
{
    s32 i;
    u32 *ret = ((void *)0) ;
    OSIntrMode e;
    e = OS_DisableInterrupts();
    if (wmspW.wm7buf != ((void *)0) ) {
        for (i = 0; i < 32; i++) {
            if (wmspW.wm7buf->requestBuf[i * 4] & 0x8000 ) {
                ret = &(wmspW.wm7buf->requestBuf[i * 4]);
                *ret &= ~(0x8000 );
                break;
            }
        }
    }
    (void)OS_RestoreInterrupts(e);
    return ret;
}
