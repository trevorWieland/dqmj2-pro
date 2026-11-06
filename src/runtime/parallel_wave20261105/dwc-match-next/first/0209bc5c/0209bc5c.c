#include "context.h"
BOOL native_main_0209bc5c(u8 aid)
{
    if (!stpDwcCnt) return FALSE;
    if (!(stpDwcCnt->matchcnt.validAidBitmap & (1 << aid))) return FALSE;

    return DWCi_IsValidAID(aid);
}