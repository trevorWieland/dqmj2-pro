#include "context.h"
BOOL native_main_0209f334 (DWCError error, int errorCode, int profileID)
{
#pragma unused(profileID)
    if (native_fn_0209bc88() != DWC_STATE_MATCHING) return FALSE;
    if (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_SC_SV) {
        DWC_Printf(DWC_REPORTFLAG_DEBUG, "DWCi_ProcessMatchClosing: SC_SV.\n");
        return TRUE;
    }
    if (error) {
        native_fn_0209f130(error, errorCode + DWC_ECODE_SEQ_MATCH);
        return TRUE;
    }
    native_fn_020a3d70()->aidList[0] = 0;
    if ((native_fn_020a3d70()->cancelState == DWC_MATCH_CANCEL_STATE_EXEC) ||
        (native_fn_020a3d70()->closeState == DWC_MATCH_CLOSE_STATE_CHANGE_TO_CLIENT) ||
        (native_fn_020a3d70()->closeState == DWC_MATCH_CLOSE_STATE_TIMEOUT))
        return TRUE;
    if (native_fn_020a3d70()->nnInfo.cookie) {
        native_fn_020b6c90(native_fn_020a3d70()->nnInfo.cookie);
        native_fn_020a3d70()->nnInfo.cookie = 0;
    }
    if (native_fn_020a3d70()->gt2NumConnection) {
        if (native_fn_020a3d70()->closeState == DWC_MATCH_CLOSE_STATE_INIT) {
            native_fn_020a3d70()->closeState = DWC_MATCH_CLOSE_STATE_FORCED;
            native_fn_020b4540(*native_fn_020a3d70()->pGt2Socket);
        }
    } else {
        if (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_SC_CL) {
            native_fn_0209f130(DWC_ERROR_NETWORK,
                              DWC_ECODE_SEQ_MATCH + DWC_ECODE_TYPE_SC_CL_FAIL);
        } else if (native_fn_020a3d70()->priorProfileID)   {
            DWC_Printf(DWC_REPORTFLAG_MATCH_NN, "Reserve NN to %u.\n",
                       native_fn_020a3d70()->priorProfileID);
            (void)native_fn_020a22b4();
        } else if (native_fn_020a3d70()->state == DWC_MATCH_STATE_CL_WAITING)   {
            DWC_Printf(DWC_REPORTFLAG_MATCH_NN, "Wait prior profileID.\n");
            native_fn_020a3d7c(DWC_MATCH_STATE_WAIT_CLOSE);
            native_fn_020a3d70()->closedTime = native_fn_02007a9c();
        } else {
            DWC_Printf(DWC_REPORTFLAG_MATCH_NN, "Restart matching immediately.\n");
            native_fn_020a21e0(DWC_MATCH_RESET_RESTART);
        }
    }
    return TRUE;
}
