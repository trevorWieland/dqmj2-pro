#include "context.h"
void native_main_0209d758 (GPConnection * connection, GPProfileSearchResponseArg * arg, void * param)
{
    int idx;
    GPResult gpResult;
    int friendIdx = (int)param;

    DWC_Printf(DWC_REPORTFLAG_DEBUG, "ProfileSearch: num:%d m:%x\n", arg->numMatches, arg->more);

    if ((arg->result == GP_NO_ERROR) && arg->numMatches &&
        (DWC_GetFriendDataType(&stpFriendCnt->friendList[friendIdx]) != DWC_FRIENDDATA_NODATA)) {
        int match_index;

        if (arg->numMatches > 1) {
            DWC_Printf(DWC_REPORTFLAG_UPDATE_SV, "Happned to find %d profiles.\n",
                       arg->numMatches);
        }

        if (stpFriendCnt->state == DWC_FRIEND_STATE_PERS_LOGIN) {
            for (match_index = 0 ; match_index < arg->numMatches ; ++match_index) {
                if (DWCi_RefreshFriendListForth(stpFriendCnt->friendList,
                                                friendIdx,
                                                arg->matches[match_index].profile)) {

                    stpFriendCnt->buddyUpdateIdx++;
                    stpFriendCnt->buddyUpdateState = DWC_BUDDY_UPDATE_STATE_CHECK;
                    arg->more = GP_DONE;

                    return;
                }
            }

            for (match_index = 0 ; match_index < arg->numMatches ; ++match_index) {
                gpResult = gpGetBuddyIndex(connection, arg->matches[match_index].profile, &idx);
                (void)DWCi_HandleGPError(gpResult);

                if (idx == -1) {
                    (void)DWCi_GPSendBuddyRequest(arg->matches[match_index].profile);
                    native_fn_02096e50(&stpFriendCnt->friendList[friendIdx], TRUE);
                } else {
                    DWC_SetGsProfileId(&stpFriendCnt->friendList[friendIdx], arg->matches->profile);
                    DWCi_SetBuddyFriendData(&stpFriendCnt->friendList[friendIdx]);
                    native_fn_02096e08(&stpFriendCnt->friendList[friendIdx], TRUE);
                    if (native_fn_02096d04(&stpFriendCnt->friendList[friendIdx]))
                        native_fn_02096e2c(&stpFriendCnt->friendList[friendIdx], TRUE);
                    DWCi_CallBuddyFriendCallback(friendIdx);

                    stpFriendCnt->buddyUpdateIdx++;
                    stpFriendCnt->buddyUpdateState = DWC_BUDDY_UPDATE_STATE_CHECK;
                    arg->more = GP_DONE;
                    stpFriendCnt->friendListChanged = 1;
                    return;
                }
            }

            if (arg->more != GP_MORE) {
                stpFriendCnt->buddyUpdateIdx++;
                stpFriendCnt->buddyUpdateState = DWC_BUDDY_UPDATE_STATE_CHECK;
            } else {
                DWC_Printf(DWC_REPORTFLAG_DEBUG, "more profiles will come...\n");
            }
        }
    } else if (arg->result)   {
        if (DWCi_HandleGPError(arg->result)) return;
    } else if ((stpFriendCnt->state == DWC_FRIEND_STATE_PERS_LOGIN) ||
               (DWC_GetFriendDataType(&stpFriendCnt->friendList[friendIdx]) == DWC_FRIENDDATA_NODATA)) {

        stpFriendCnt->buddyUpdateIdx++;
        stpFriendCnt->buddyUpdateState = DWC_BUDDY_UPDATE_STATE_CHECK;
    }
}
