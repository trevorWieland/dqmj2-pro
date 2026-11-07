#include "context.h"
BOOL native_main_020a40c0 (DWCUserRecvCallback callback)
{
    if (sTransInfo == NULL) return FALSE;

    sTransInfo->recvCallback = callback;
    return TRUE;
}
