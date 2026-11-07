#include "context.h"
void native_main_0209e258 (const u8 friendIdxList[],
                                 int friendIdxListLen,
                                 u8 numEntry,
                                 BOOL distantFriend,
                                 DWCMatchedSCCallback matchedCallback,
                                 void * matchedParam,
                                 DWCEvalPlayerCallback evalCallback,
                                 void * evalParam)
{
    char valueStr[12], keyValueStr[32];
#ifndef DWC_MATCH_ACCEPT_NO_FRIEND
    int checkpid;
    int friendCount;
    int i;
#endif
    int result;
    GPResult gpResult;

    DWCi_SetMatchCommonParam(DWC_MATCH_TYPE_FRIEND,
                             numEntry, matchedCallback, matchedParam);

    DWCi_GetMatchCnt()->distantFriend = (u8)(distantFriend ? 1 : 0);
    DWCi_GetMatchCnt()->evalCallback = evalCallback;
    DWCi_GetMatchCnt()->evalParam = evalParam;

#ifdef DWC_MATCH_ACCEPT_NO_FRIEND
    MI_CpuCopy8(friendIdxList, DWCi_GetMatchCnt()->friendIdxList, (u32)friendIdxListLen);
    DWCi_GetMatchCnt()->friendIdxListLen = friendIdxListLen;

    if (!friendIdxListLen ||
        ((friendIdxListLen < numEntry) &&
         !distantFriend &&
         (!stpOptMinComp || !stpOptMinComp->valid || (friendIdxListLen < stpOptMinComp->minEntry - 1)))) {

        DWCi_StopMatching(DWC_ERROR_FRIENDS_SHORTAGE, 0);
        return;
    }
#else
    for (i = 0, friendCount = 0; i < friendIdxListLen; i++) {
        if (!(checkpid = DWCi_GetProfileIDFromList(friendIdxList[i])) ||
            !gpIsBuddy(DWCi_GetMatchCnt()->pGpObj, checkpid)) {

            continue;
        }

        DWCi_GetMatchCnt()->friendIdxList[friendCount] = friendIdxList[i];
        friendCount++;
    }

    if (!friendCount ||
        ((friendCount < numEntry) &&
         !distantFriend &&
         (!stpOptMinComp || !stpOptMinComp->valid || (friendCount < stpOptMinComp->minEntry - 1)))) {

        DWCi_StopMatching(DWC_ERROR_FRIENDS_SHORTAGE, 0);
        return;
    }

    DWCi_GetMatchCnt()->friendIdxListLen = friendCount;
#endif
    DWCi_SetMatchStatus(DWC_MATCH_STATE_CL_WAIT_RESV);

    if (!DWCi_GetMatchCnt()->sbObj)
        DWCi_GetMatchCnt()->sbObj = ServerBrowserNew(DWCi_GetMatchCnt()->gameName,
                                                     DWCi_GetMatchCnt()->gameName,
                                                     DWCi_GetMatchCnt()->secretKey, 0, 20,
                                                     QVERSION_QR2, SBFalse,
                                                     DWCi_SBCallback, NULL);
    if (!DWCi_GetMatchCnt()->sbObj) {
        if (DWCi_HandleSBError(sbe_allocerror)) return;
    }

    (void)OS_SNPrintf(valueStr, sizeof(valueStr), native_data_020e01a4, numEntry);
    (void)DWC_SetCommonKeyValueString(DWC_GP_SSTR_KEY_MATCH_FRIEND_NUM, valueStr, keyValueStr, '/');
    (void)DWC_AddCommonKeyValueString(DWC_GP_SSTR_KEY_DISTANT_FRIEND, distantFriend ? native_data_020e01ac : native_data_020e01b0, keyValueStr, '/');

    (void)OS_SNPrintf(valueStr, sizeof(valueStr), native_data_020e01a4, DWC_MATCHING_VERSION);
    (void)DWC_AddCommonKeyValueString(DWC_GP_SSTR_KEY_MATCH_VERSION, valueStr, keyValueStr, '/');

    gpResult = DWCi_SetGPStatus(DWC_STATUS_MATCH_FRIEND, keyValueStr, NULL);
    if (DWCi_HandleGPError(gpResult)) return;

#ifdef DWC_QR2_ALIVE_DURING_MATCHING
    if (DWCi_GetMatchCnt()->qr2Obj == NULL) {
        if (DWCi_QR2Startup(DWCi_GetMatchCnt()->profileID)) return;
    }
#else
    qr2_send_statechanged(DWCi_GetMatchCnt()->qr2Obj);
#endif
    result = DWCi_SendResvCommandToFriend(FALSE, TRUE, 0);
    if (DWCi_HandleMatchCommandError(result)) return;

    DWCi_InitOptMinCompParam(FALSE);
}
