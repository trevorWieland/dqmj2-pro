#include "context.h"
BOOL native_main_020a40a4 (DWCUserSendCallback callback)
{
    if (sTransInfo == NULL) return FALSE;

    sTransInfo->sendCallback = callback;
    return TRUE;
}
