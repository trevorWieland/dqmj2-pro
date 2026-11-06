#include "context.h"
BOOL native_main_0209d690(const DWCFriendData * friendData, GPBuddyStatus * status)
{
    u8 ret;
    int buddyIdx = 0;
    int profileid;

    SDK_ASSERT(friendData);
    SDK_ASSERT(status);

    if (!stpFriendCnt || !DWCi_CheckLogin()) return FALSE;

    profileid = DWC_GetGsProfileId(DWCi_GetUserData(), friendData);
    if (profileid > 0 && gpGetBuddyIndex(stpFriendCnt->pGpObj,
                                         profileid,
                                         &buddyIdx)) {
        ret = FALSE;
    } else if (profileid <= 0 || buddyIdx == -1)   {
        ret = FALSE;
    } else {
        if (gpGetBuddyStatus(stpFriendCnt->pGpObj, buddyIdx, status)) {
            ret = FALSE;
        } else {
            ret = TRUE;
        }
    }

    return ret;
}