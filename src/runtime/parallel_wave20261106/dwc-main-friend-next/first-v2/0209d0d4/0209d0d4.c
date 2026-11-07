#include "context.h"
void native_main_0209d0d4 (GPConnection * connection, GPRecvBuddyStatusArg * arg, void * param)
{
#pragma unused(param)
    int friendIdx;
    GPBuddyStatus status;

    DWC_Printf(DWC_REPORTFLAG_UPDATE_SV, "RECV update friend status. p:%d\n", arg->profile);

    if (stpFriendCnt->statusCallback) {
        friendIdx = DWCi_GetFriendListIndex(arg->profile);
        if (friendIdx == -1) {
            return;
        }

        (void)gpGetBuddyStatus(connection, arg->index, &status);

        stpFriendCnt->statusCallback(friendIdx,
                                     (u8)status.status,
                                     status.locationString,
                                     stpFriendCnt->statusParam);
    }
}
