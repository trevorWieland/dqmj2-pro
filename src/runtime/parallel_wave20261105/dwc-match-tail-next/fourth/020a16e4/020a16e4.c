#include "context.h"
BOOL native_main_020a16e4 (int clientPid)
{
    int i;
    BOOL isServer;
    if (native_fn_020a3d70()->qr2IsReserved && (native_fn_020a3d70()->qr2Reservation == native_fn_020a3d70()->profileID)) {
        DWC_Printf(DWC_REPORTFLAG_DEBUG,
                   "DWCi_CancelPreConnectedServerProcess : client\n");
        isServer = FALSE;
    } else {
        DWC_Printf(DWC_REPORTFLAG_DEBUG,
                   "DWCi_CancelPreConnectedServerProcess : server\n");
        isServer = TRUE;
    }
    if (isServer) {
        native_fn_020a3d70()->qr2IsReserved = 0;
        native_fn_020a3d70()->qr2Reservation = 0;
        native_fn_020b748c(native_fn_020a3d70()->qr2Obj);
    }
    if (native_fn_020a3d70()->gt2NumConnection < DWC_MAX_CONNECTIONS - 1) {
        native_fn_020a3d70()->sbPidList[native_fn_020a3d70()->gt2NumConnection + 1] = 0;
    }
    native_fn_020a3d70()->cmdCnt.command = DWC_MATCH_COMMAND_DUMMY;
    if (native_fn_020a3d70()->nnInfo.cookie) {
        native_fn_020b6c90(native_fn_020a3d70()->nnInfo.cookie);
        native_fn_020a3d70()->nnInfo.cookie = 0;
    }
    native_fn_020a3d70()->qr2NNFinishCount = (u8)native_fn_020a3d70()->gt2NumConnection;
    native_fn_020a3d70()->reqProfileID = 0;
    if (!isServer) {
        if (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_SC_CL) {
        } else {
            native_fn_020a2290();
        }
    } else if (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_ANYBODY)   {
        native_fn_020a3d7c(DWC_MATCH_STATE_CL_SEARCH_HOST);
        native_fn_020a3d70()->sbUpdateFlag = DWC_SB_UPDATE_INTERVAL_LONG;
        native_fn_020a3d70()->sbUpdateTick = native_fn_02007a9c();
    } else if (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_FRIEND)   {
        native_fn_020a3d7c(DWC_MATCH_STATE_CL_WAIT_RESV);
        (void)native_fn_020a13d8(TRUE, FALSE, 0);
    } else if (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_SC_SV)   {
        native_fn_020a3d7c(DWC_MATCH_STATE_SV_CANCEL_SYN);
        native_fn_020a3d70()->cancelSynAckBit = 0;
        native_fn_020a3d70()->cancelBaseLatency = 0;
        native_fn_020a233c(clientPid);
        for (i = 1; i <= native_fn_020a3d70()->gt2NumConnection; i++) {
            if (!native_fn_020a2724(native_fn_020a3d70()->sbPidList[i],
                                                DWC_MATCH_COMMAND_CANCEL_SYN))
                return FALSE;
        }
        if (native_fn_020a3d70()->gt2NumConnection == 0) {
            native_fn_020a21e0(DWC_MATCH_RESET_CONTINUE);
        }
    }
    return TRUE;
}
