#include "context.h"
BOOL native_main_020a2544 (void)
{
    u64 passTime;
    int i;
    if ((native_fn_020a3d70()->state == DWC_MATCH_STATE_CL_SYN) ||
        (native_fn_020a3d70()->state == DWC_MATCH_STATE_SV_SYN) ||
        (native_fn_020a3d70()->state == DWC_MATCH_STATE_SV_SYN_WAIT))
        passTime = OS_TicksToMilliSeconds(native_fn_02007a9c() - native_fn_020a3d70()->lastSynSent);
    else return TRUE;
    switch (native_fn_020a3d70()->state) {
    case DWC_MATCH_STATE_CL_SYN:
        if (passTime > DWC_MATCH_SYN_ACK_WAIT_TIME) {
            DWC_Printf(DWC_REPORTFLAG_MATCH_GT2, "[SYN] No ACK from server %d/%d.\n",
                       native_fn_020a3d70()->clWaitTimeoutCount, DWC_MATCH_CMD_RETRY_MAX);
            if ((native_fn_0209bc88() == DWC_STATE_MATCHING) &&
                (native_fn_020a3d70()->clWaitTimeoutCount >= DWC_MATCH_CMD_RETRY_MAX)) {
                DWC_Printf(DWC_REPORTFLAG_MATCH_GT2,
                           "Timeout: [SYN] Connection to server was shut down.\n");
                if (!native_fn_020a1878(native_fn_020a3d70()->sbPidList[0]))
                    return FALSE;
            } else {
                native_fn_020a3d70()->clWaitTimeoutCount++;
                native_fn_020a249c(native_fn_020a3d70()->aidList[0],
                                        DWC_SEND_TYPE_MATCH_SYN_ACK);
            }
        }
        break;
    case DWC_MATCH_STATE_SV_SYN:
        if (passTime > DWC_MATCH_SYN_ACK_WAIT_TIME) {
            native_fn_020a3d70()->synResendCount++;
            if (native_fn_020a3d70()->synResendCount > DWC_MATCH_CMD_RETRY_MAX) {
                DWC_Printf(DWC_REPORTFLAG_MATCH_NN,
                           "Timeout: wait SYN-ACK (aidbitmap 0x%x). Restart matching.\n",
                           native_fn_020a3d70()->synAckBit);
                if ((native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_ANYBODY) ||
                    (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_FRIEND)) {
                    native_fn_020a2394();
                    native_fn_020a21e0(DWC_MATCH_RESET_RESTART);
                } else {
                    if (!native_fn_020a23bc(native_fn_020a3d70()->synAckBit))
                        return FALSE;
                    if (native_fn_020a3d70()->gt2NumConnection != 0) {
                        native_fn_020a3d70()->synResendCount = 0;
                        native_fn_020a3d70()->lastSynSent = native_fn_02007a9c();
                    } else {
                        if (!native_fn_020a16e4(native_fn_020a3d70()->cbEventPid))
                            return FALSE;
                    }
                }
            } else {
                for (i = 1; i <= native_fn_020a3d70()->gt2NumConnection; i++) {
                    if (!(native_fn_020a3d70()->synAckBit & (1u << native_fn_020a3d70()->aidList[i]))) {
                        native_fn_020a249c(native_fn_020a3d70()->aidList[i],
                                                DWC_SEND_TYPE_MATCH_SYN);
                    }
                }
            }
        }
        break;
    case DWC_MATCH_STATE_SV_SYN_WAIT:
        if (passTime > native_fn_020a3d70()->baseLatency) {
            native_fn_020a19b4(DWC_PP_CONNECTION_SYN_FINISH);
        }
        break;
    }
    return TRUE;
}
