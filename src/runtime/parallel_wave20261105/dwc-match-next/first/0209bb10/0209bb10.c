#include "context.h"
BOOL native_main_0209bb10(DWCConnectionClosedCallback callback, void * param)
{
    if (!stpDwcCnt) return FALSE;

    stpDwcCnt->closedCallback = callback;
    stpDwcCnt->closedParam = param;

    return TRUE;
}