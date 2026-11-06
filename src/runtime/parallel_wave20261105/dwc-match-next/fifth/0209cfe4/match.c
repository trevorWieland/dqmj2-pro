#include "context.h"
void native_main_0209cfe4(const char * authToken,
                              const char * partnerChallenge,
                              DWCUpdateServersCallback updateCallback,
                              void * updateParam,
                              DWCFriendStatusCallback statusCallback,
                              void * statusParam,
                              DWCDeleteFriendListCallback deleteCallback,
                              void * deleteParam)
{
#pragma unused(authToken)
#pragma unused(partnerChallenge)

    SDK_ASSERT(updateCallback);

    stpFriendCnt->updateCallback = updateCallback;
    stpFriendCnt->updateParam = updateParam;
    stpFriendCnt->statusCallback = statusCallback;
    stpFriendCnt->statusParam = statusParam;
    stpFriendCnt->deleteCallback = deleteCallback;
    stpFriendCnt->deleteParam = deleteParam;

    stpFriendCnt->friendListChanged = 0;

    stpFriendCnt->buddyUpdateState = DWC_BUDDY_UPDATE_STATE_WAIT;
    stpFriendCnt->svUpdateComplete = 0;
    stpFriendCnt->buddyUpdateIdx = 0;

    stpFriendCnt->state = DWC_FRIEND_STATE_PERS_LOGIN;

    if (stpFriendCnt->friendList == NULL) {
        stpFriendCnt->svUpdateComplete++;
    }

    stpFriendCnt->svUpdateComplete++;
}