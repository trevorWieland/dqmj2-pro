#include "context.h"
int native_main_020a13d8 (BOOL delay, BOOL init, int resendPid)
{
    char version[12];
    char numEntry[4];
    char distantFriend[2];
    int profileID;
    int startIdx = init ? native_fn_020a3d70()->friendCount :
                   (native_fn_020a3d70()->friendCount < native_fn_020a3d70()->friendIdxListLen - 1) ? native_fn_020a3d70()->friendCount + 1 : 0;
    int buddyIdx;
    int initFinished = 0;
    int versionLen, numEntryLen, distantFriendLen;
    int i;
    GPBuddyStatus status;
    GPResult gpResult;
    while (1) {
        if (!init || initFinished) {
            native_fn_020a3d70()->friendCount++;
            if (native_fn_020a3d70()->friendCount >= native_fn_020a3d70()->friendIdxListLen) {
                native_fn_020a3d70()->friendCount = 0;
            }
        }
        if (initFinished) {
            if (native_fn_020a3d70()->friendCount == startIdx) {
                native_fn_020a3d70()->cmdTimeoutTime = DWC_MATCH_CMD_RESEND_INTERVAL_MSEC;
                native_fn_020a3d70()->cmdTimeoutStartTick = native_fn_02007a9c();
                native_fn_020a3d70()->cmdResendFlag = FALSE;
                return 0;
            }
        }
        initFinished = 1;
        profileID = native_fn_020972f4(native_fn_0209c5fc(), &native_fn_020a3d70()->friendList[native_fn_020a3d70()->friendIdxList[native_fn_020a3d70()->friendCount]]);
#ifdef DWC_MATCH_ACCEPT_NO_FRIEND
        if ((profileID == 0) || (profileID == -1)) continue;
        if (!native_fn_020971ac(&native_fn_020a3d70()->friendList[native_fn_020a3d70()->friendIdxList[native_fn_020a3d70()->friendCount]])) continue;
#endif
        for (i = 1; i <= native_fn_020a3d70()->gt2NumConnection; i++) {
            if (native_fn_020a3d70()->sbPidList[i] == profileID) break;
        }
        if (i > native_fn_020a3d70()->gt2NumConnection) {
            gpResult = native_fn_020aa4f0(native_fn_020a3d70()->pGpObj, profileID, &buddyIdx);
            gpResult |= native_fn_020aa3e0(native_fn_020a3d70()->pGpObj, buddyIdx, &status);
            if (!gpResult && (status.status == DWC_STATUS_MATCH_FRIEND)) {
                versionLen =
                    native_fn_0209b2bc(DWC_GP_SSTR_KEY_MATCH_VERSION,
                                             version,
                                             status.statusString,
                                             '/');
                numEntryLen =
                    native_fn_0209b2bc(DWC_GP_SSTR_KEY_MATCH_FRIEND_NUM,
                                             numEntry,
                                             status.statusString,
                                             '/');
                distantFriendLen =
                    native_fn_0209b2bc(DWC_GP_SSTR_KEY_DISTANT_FRIEND,
                                             distantFriend,
                                             status.statusString,
                                             '/');
                if ((versionLen > 0) && (numEntryLen > 0) && (distantFriendLen > 0) &&
                    (strtoul(version, NULL, 10) == DWC_MATCHING_VERSION) &&
                    (strtoul(numEntry, NULL, 10) == native_fn_020a3d70()->qr2NumEntry)) {
                    break;
                }
            }
        }
    }
    if (profileID == resendPid) delay = TRUE;
    return native_fn_020a1278(profileID, delay);
}
