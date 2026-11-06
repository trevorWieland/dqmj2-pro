#include "context.h"
void native_main_0209d4c0(void)
{
    stpFriendCnt->updateCallback(DWC_ERROR_NONE,
                                 stpFriendCnt->friendListChanged,
                                 stpFriendCnt->updateParam);

    stpFriendCnt->state = DWC_FRIEND_STATE_LOGON;
}