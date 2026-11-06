#include "context.h"
GPResult native_main_0209becc (GPResult result)
{
    int errorCode;
    DWCError dwcError;

    if (result == GP_NO_ERROR) return GP_NO_ERROR;

    DWC_Printf(DWC_REPORTFLAG_ERROR, "Main, GP error %d\n", result);

    switch (result) {
    case GP_MEMORY_ERROR:
        dwcError = DWC_ERROR_FATAL;
        errorCode = DWC_ECODE_TYPE_ALLOC;
        break;
    case GP_PARAMETER_ERROR:
        dwcError = DWC_ERROR_FATAL;
        errorCode = DWC_ECODE_TYPE_PARAM;
        break;
    case GP_NETWORK_ERROR:
        dwcError = DWC_ERROR_NETWORK;
        errorCode = DWC_ECODE_TYPE_NETWORK;
        break;
    case GP_SERVER_ERROR:
        dwcError = DWC_ERROR_NETWORK;
        errorCode = DWC_ECODE_TYPE_SERVER;
        break;
    }

    switch (stpDwcCnt->state) {
    case DWC_STATE_AVAILABLE_CHECK:
        errorCode += DWC_ECODE_SEQ_LOGIN + DWC_ECODE_GS_GP;
        DWCi_StopLogin(dwcError, errorCode);
        break;
    case DWC_STATE_LOGIN:
        errorCode += DWC_ECODE_SEQ_LOGIN + DWC_ECODE_GS_GP;

        if (stpDwcCnt->logcnt.state < DWC_LOGIN_STATE_REMOTE_AUTH) {
            DWCi_StopLogin(dwcError, errorCode);
        } else {
            DWC_Printf(DWC_REPORTFLAG_ERROR, "Not handle an error here.\n");
        }
        break;
    case DWC_STATE_MATCHING:
        errorCode += DWC_ECODE_SEQ_MATCH + DWC_ECODE_GS_GP;
        DWCi_StopMatching(dwcError, errorCode);
        break;
    case DWC_STATE_UPDATE_SERVERS:
        errorCode += DWC_ECODE_SEQ_FRIEND + DWC_ECODE_GS_GP;
        break;
    default:
        errorCode += DWC_ECODE_SEQ_ETC + DWC_ECODE_GS_GP;
        break;
    }

    DWCi_StopFriendProcess(dwcError, errorCode);
    return result;
}