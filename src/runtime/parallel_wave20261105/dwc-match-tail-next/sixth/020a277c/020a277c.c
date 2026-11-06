#include "context.h"
BOOL native_main_020a277c (int profileID, u8 command, u32 data)
{
    u8 aid;
    u32 bitmask;
    u64 baseTime, latency;
    int i;
    DWC_Printf(DWC_REPORTFLAG_MATCH_GT2, "Received CANCEL SYN %d command from %u.\n",
               command - DWC_MATCH_COMMAND_CANCEL_SYN, profileID);
    if (native_fn_0209bc88() != DWC_STATE_CONNECTED) {
        DWC_Printf(DWC_REPORTFLAG_MATCH_GT2, "Ignore delayed CANCEL SYN.\n");
        return TRUE;
    }
    switch (command) {
    case DWC_MATCH_COMMAND_CANCEL_SYN:
        if (native_fn_020a3d70()->state != DWC_MATCH_STATE_CL_CANCEL_SYN) {
            native_fn_020a3d7c(DWC_MATCH_STATE_CL_CANCEL_SYN);
            native_fn_020a233c((int)data);
        }
        if (!native_fn_020a2724(profileID, DWC_MATCH_COMMAND_CANCEL_SYN_ACK))
            return FALSE;
        break;
    case DWC_MATCH_COMMAND_CANCEL_SYN_ACK:
        if (native_fn_020a3d70()->state == DWC_MATCH_STATE_SV_CANCEL_SYN) {
            baseTime = native_fn_02007a9c();
            if ((OS_TicksToMilliSeconds(baseTime - native_fn_020a3d70()->lastCancelSynSent) >> 1) > DWC_GP_PROCESS_INTERVAL) {
                latency = (OS_TicksToMilliSeconds(baseTime - native_fn_020a3d70()->lastCancelSynSent) >> 1) - DWC_GP_PROCESS_INTERVAL;
                if (latency > native_fn_020a3d70()->cancelBaseLatency) {
                    native_fn_020a3d70()->cancelBaseLatency = (u16)latency;
                }
            }
            aid = native_fn_020a2c38(profileID, FALSE);
            if (aid != 0xff) {
                native_fn_020a3d70()->cancelSynAckBit |= 1u << aid;
            }
            bitmask = native_fn_020a2c80(TRUE);
            if (native_fn_020a3d70()->cancelSynAckBit == bitmask) {
                for (i = 1; i <= native_fn_020a3d70()->gt2NumConnection; i++) {
                    if (!native_fn_020a2724(native_fn_020a3d70()->sbPidList[i],
                                                        DWC_MATCH_COMMAND_CANCEL_ACK))
                        return FALSE;
                }
                native_fn_020a3d7c(DWC_MATCH_STATE_SV_CANCEL_SYN_WAIT);
                DWC_Printf(DWC_REPORTFLAG_MATCH_GT2,
                           "Wait max latency %d msec.\n",
                           native_fn_020a3d70()->cancelBaseLatency);
            }
        } else {
            if (!native_fn_020a2724(profileID, DWC_MATCH_COMMAND_CANCEL_ACK))
                return FALSE;
        }
        break;
    case DWC_MATCH_COMMAND_CANCEL_ACK:
        if (native_fn_020a3d70()->state == DWC_MATCH_STATE_CL_CANCEL_SYN) {
            native_fn_020a21e0(DWC_MATCH_RESET_CONTINUE);
        }
        break;
    }
    return TRUE;
}
