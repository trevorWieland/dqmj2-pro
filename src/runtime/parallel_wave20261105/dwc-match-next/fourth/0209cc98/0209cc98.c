#include "context.h"
u8 native_main_0209cc98(const DWCFriendData * friendData, u8 * maxEntry, u8 * numEntry, char * statusData, int * size)
{
    u8 ret;
    char statusString[DWC_GS_STATUS_STRING_LEN];

    ret = DWC_GetFriendStatusSC(friendData, maxEntry, numEntry, statusString);

    if (ret == DWC_STATUS_OFFLINE) {
        *size = -1;
        return ret;
    }

    *size = DWC_Auth_Base64Decode(statusString, strlen(statusString), NULL, 0);

    if (!statusData || (*size == -1)) return ret;

    (void)DWC_Auth_Base64Decode(statusString, strlen(statusString), statusData, (u32) * size);

    return ret;
}