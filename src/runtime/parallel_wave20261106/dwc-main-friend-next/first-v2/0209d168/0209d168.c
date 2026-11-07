#include "context.h"
int native_main_0209d168 (int profileID)
{
    int i;

    if (!stpFriendCnt || !profileID) return -1;

    for (i = 0; i < stpFriendCnt->friendListLen; i++) {
        if (DWCi_GetProfileIDFromList(i) == profileID) {
            return i;
        }
    }

    return -1;
}
