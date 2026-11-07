#include "context.h"
void native_main_0209d238 (int index)
{
    if (stpFriendCnt->buddyCallback &&
        (stpFriendCnt->state != DWC_FRIEND_STATE_PERS_LOGIN)) {
        stpFriendCnt->buddyCallback(index, stpFriendCnt->buddyParam);
    }

    if (stpFriendCnt->statusCallback) {
        u8 st;
        GPBuddyStatus status;

        st = DWC_GetFriendStatus(&stpFriendCnt->friendList[index], status.locationString);

        stpFriendCnt->statusCallback(index,
                                     st,
                                     status.locationString,
                                     stpFriendCnt->statusParam);
    }
}
