#include "context.h"
BOOL native_main_0209d514(DWCFriendData friendList[], int index, int profileID)
{
    int pid_i;
    int i;

    if (DWC_GetFriendDataType(&friendList[index]) == 1) return FALSE;

    for (i = 0; i < index; i++) {
        pid_i = DWCi_GetProfileIDFromList(i);
        if (pid_i && (pid_i == profileID)) {

            DWC_Printf(DWC_REPORTFLAG_UPDATE_SV,
                       "Found same friend in the list [%d] & [%d], %d\n",
                       i, index, DWC_GetFriendDataType(&friendList[i]));

            if (DWC_IsBuddyFriendData(&friendList[index]) &&
                !DWC_IsBuddyFriendData(&friendList[i])) {
                DWCi_DeleteFriendFromList(friendList, i, index);
            } else {
                DWCi_DeleteFriendFromList(friendList, index, i);
            }

            stpFriendCnt->friendListChanged = 1;
            return TRUE;
        }
    }

    return FALSE;
}