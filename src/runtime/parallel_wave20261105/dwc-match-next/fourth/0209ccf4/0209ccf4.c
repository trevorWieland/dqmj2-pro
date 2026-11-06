#include "context.h"
BOOL native_main_0209ccf4(const char * statusData, u32 size)
{
    char statusString[DWC_GS_STATUS_STRING_LEN];
    int len;

    if (!stpFriendCnt || !DWCi_CheckLogin()) return FALSE;

    len = DWC_Auth_Base64Encode(statusData, size,
                                statusString, DWC_GS_STATUS_STRING_LEN - 1);

    if (len == -1) return FALSE;

    statusString[len] = '\0';

    if (DWCi_SetGPStatus(DWC_GP_STATUS_NO_CHANGE, NULL, statusString)) return FALSE;
    else return TRUE;
}