#include "context.h"
BOOL native_main_0209ba08(const u8 friendIdxList[],
                                int friendIdxListLen,
                                u8 numEntry,
                                BOOL distantFriend,
                                DWCMatchedCallback matchedCallback,
                                void * matchedParam,
                                DWCEvalPlayerCallback evalCallback,
                                void * evalParam)
{
    u8 tmpFriendIdxList[DWC_MAX_MATCH_IDX_LIST];
    u8 idxList[DWC_MAX_MATCH_IDX_LIST];
    u8 i;
    u32 j;

    SDK_ASSERT(stpDwcCnt);
    SDK_ASSERT(friendIdxListLen <= DWC_MAX_MATCH_IDX_LIST);
    SDK_ASSERT((numEntry > 1) && (numEntry <= DWC_MAX_CONNECTIONS));
    SDK_ASSERT(matchedCallback);

    DWC_Printf(DWC_REPORTFLAG_DEBUG, "!!DWC_ConnectToFriendsAsync() was called!!\n");

    if (DWCi_IsError() || (stpDwcCnt->state != DWC_STATE_ONLINE)) {
        DWC_Printf(DWC_REPORTFLAG_DEBUG, "But ignored.\n");
        return FALSE;
    }

    DWCi_ClearGT2ConnectionList();

    stpDwcCnt->matchedCallback = matchedCallback;
    stpDwcCnt->matchedParam = matchedParam;

    DWCi_SetState(DWC_STATE_MATCHING);

    if (friendIdxList) {
        DWCi_ConnectToFriendsAsync(friendIdxList, friendIdxListLen,
                                   (u8)(numEntry - 1),
                                   distantFriend,
                                   DWCi_MatchedCallback, NULL,
                                   evalCallback, evalParam);
    } else {
        friendIdxListLen = 0;

        for (i = 0; i < DWCi_GetFriendListLen(); i++) {
            idxList[i] = i;
        }

        for (i = 0; i < DWCi_GetFriendListLen(); i++) {
            u32 randIdx = DWCi_GetMathRand32((u32)(DWCi_GetFriendListLen() - i));

#ifdef DWC_MATCH_ACCEPT_NO_FRIEND
            tmpFriendIdxList[i] = idxList[randIdx];
            friendIdxListLen++;
#else
            if (DWCi_Acc_IsValidFriendData(&(DWCi_GetFriendList())[idxList[randIdx]])) {
                tmpFriendIdxList[i] = idxList[randIdx];
                friendIdxListLen++;
            }
#endif
            for (j = randIdx; j < DWCi_GetFriendListLen() - i - 1; j++) {
                idxList[j] = idxList[j + 1];
            }
        }

        DWCi_ConnectToFriendsAsync(tmpFriendIdxList, friendIdxListLen,
                                   (u8)(numEntry - 1),
                                   distantFriend,
                                   DWCi_MatchedCallback, NULL,
                                   evalCallback, evalParam);
    }

    return TRUE;
}