#include "context.h"
int native_main_020a1278 (int profileID, BOOL delay)
{
    u8 command;
    u32 senddata[3];
    int sendlen;
    int result;
    SBServer server;
    if (delay || ((native_fn_020a3d70()->qr2IP == 0) && (native_fn_020a3d70()->qr2Port == 0))) {
        native_fn_020a3d70()->cmdResendFlag = TRUE;
        native_fn_020a3d70()->cmdResendTick = native_fn_02007a9c();
        native_fn_020a3d70()->sbPidList[0] = profileID;
        native_fn_020a3d70()->reqProfileID=0;
        if (!delay) {
            DWC_Printf(DWC_REPORTFLAG_DEBUG,
                       "Delay ResvCommand - qr2IP & qr2Port = 0.\n");
        }
        return 0;
    }
    if (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_ANYBODY) {
        server = native_fn_020a699c(native_fn_020a3d70()->sbObj, 0);
        native_fn_020a3d70()->sbPidList[0] = native_fn_020a601c(server, DWC_QR2_PID_KEY_STR, 0);
        native_fn_020a3d70()->qr2IPList[0] = native_fn_020a60b0(server);
        native_fn_020a3d70()->qr2PortList[0] = native_fn_020a60b4(server);
        native_fn_020a3d70()->reqProfileID = native_fn_020a3d70()->sbPidList[0];
        sendlen = 1;
    } else {
        if (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_FRIEND) {
            native_fn_020a3d70()->sbPidList[0] = profileID;
        }
        native_fn_020a3d70()->reqProfileID = profileID;
        senddata[1] = native_fn_020a3d70()->qr2IP;
        senddata[2] = native_fn_020a3d70()->qr2Port;
        sendlen = 3;
    }
    native_fn_020a3d70()->cmdTimeoutTime = DWC_MATCH_CMD_RESV_TIMEOUT_MSEC;
    native_fn_020a3d70()->cmdTimeoutStartTick = native_fn_02007a9c();
    native_fn_020a3d70()->cmdResendFlag = FALSE;
    if (native_fn_020a3d70()->priorProfileID) {
        command = DWC_MATCH_COMMAND_RESV_PRIOR;
    } else {
        command = DWC_MATCH_COMMAND_RESERVATION;
    }
    senddata[0] = native_fn_020a3d70()->qr2MatchType;
    result = native_fn_020a00ac(command,
                                   profileID,
                                   native_fn_020a3d70()->qr2IPList[0],
                                   native_fn_020a3d70()->qr2PortList[0],
                                   senddata, sendlen);
    return result;
}
