#include "context.h"
BOOL native_main_020a40dc (DWCUserRecvTimeoutCallback callback)
{
    if (sTransInfo == NULL) return FALSE;

    sTransInfo->recvTimeoutCallback = callback;
    return TRUE;
}
