#include "context.h"
void native_main_0209f1e8 (u8 aid, u16 type, u8 * data)
{
    u8 aidIdx;
    u32 bitmask;
    int i;
    DWC_Printf(DWC_REPORTFLAG_MATCH_GT2, "Received SYN %d packet from aid %d.\n",
               type - DWC_SEND_TYPE_MATCH_SYN, aid);
    switch (type) {
    case DWC_SEND_TYPE_MATCH_SYN:
        if (native_fn_020a3d70()->state == DWC_MATCH_STATE_CL_WAITING) {
            if (data[0] == 1) {
                native_fn_020a3d70()->cbEventPid = 0;
            }
            aidIdx = data[1];
            native_fn_020a3d70()->aidList[aidIdx] = data[2];
            native_fn_020a3d70()->sbPidList[aidIdx] = native_fn_020a3d70()->profileID;
            if ((native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_ANYBODY) ||
                (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_FRIEND)) {
                native_fn_020a3d70()->qr2NumEntry = (u8)native_fn_020a3d70()->gt2NumConnection;
            }
            native_fn_020a3d70()->clWaitTimeoutCount = 0;
            native_fn_020a3d7c(DWC_MATCH_STATE_CL_SYN);
        }
        native_fn_020a249c(aid, DWC_SEND_TYPE_MATCH_SYN_ACK);
        break;
    case DWC_SEND_TYPE_MATCH_SYN_ACK:
        if (native_fn_020a3d70()->state == DWC_MATCH_STATE_SV_SYN) {
            native_fn_020a3d70()->synAckBit |= 1u << aid;
            if ((data[0] | (data[1] << 8)) > native_fn_020a3d70()->baseLatency) {
                native_fn_020a3d70()->baseLatency = (u16)(data[0] | (data[1] << 8));
            }
            bitmask = native_fn_020a2c80(FALSE);
            if (native_fn_020a3d70()->synAckBit == bitmask) {
                for (i = 1; i <= native_fn_020a3d70()->gt2NumConnection; i++) {
                    native_fn_020a249c(native_fn_020a3d70()->aidList[i],
                                            DWC_SEND_TYPE_MATCH_ACK);
                }
                native_fn_020a3d7c(DWC_MATCH_STATE_SV_SYN_WAIT);
                DWC_Printf(DWC_REPORTFLAG_MATCH_GT2,
                           "Wait max latency %d msec.\n",
                           native_fn_020a3d70()->baseLatency);
            }
        } else {
            native_fn_020a249c(aid, DWC_SEND_TYPE_MATCH_ACK);
        }
        break;
    case DWC_SEND_TYPE_MATCH_ACK:
        if (native_fn_020a3d70()->state == DWC_MATCH_STATE_CL_SYN) {
            native_fn_020a19b4(DWC_PP_CONNECTION_SYN_FINISH);
        }
        break;
    }
}
