#include "context.h"
void native_main_0209cd4c(DWCFriendData * friendData)
{
    int profileID;

    if ((stpFriendCnt != NULL) &&
        DWCi_CheckLogin() &&
        (DWCi_GetUserData() != NULL) &&
        ((profileID = DWC_GetGsProfileId(DWCi_GetUserData(), friendData)) != 0) &&
        (profileID != -1) &&
        gpIsBuddy(stpFriendCnt->pGpObj, profileID)) {

        (void)gpDeleteBuddy(stpFriendCnt->pGpObj, profileID);

        DWC_Printf(DWC_REPORTFLAG_DEBUG,
                   "DWC_DeleteBuddyFriendData : Deleted buddy.\n");
    } else {
        DWC_Printf(DWC_REPORTFLAG_DEBUG,
                   "DWC_DeleteBuddyFriendData : Only clear data.\n");
    }

    MI_CpuClear8(friendData, sizeof(DWCFriendData));
}