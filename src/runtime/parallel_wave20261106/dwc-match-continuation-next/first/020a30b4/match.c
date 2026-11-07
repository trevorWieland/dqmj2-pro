#include "context.h"
qr2_error_t native_main_020a30b4 (qr2_error_t error)
{
    int errorCode;
    DWCError dwcError;

    if (error == e_qrnoerror) return e_qrnoerror;

    DWC_Printf(DWC_REPORTFLAG_ERROR, "Match, QR2 error %d\n", error);

    switch (error) {
    case e_qrwsockerror:
        dwcError = DWC_ERROR_NETWORK;
        errorCode = DWC_ECODE_TYPE_SOCKET;
        break;
    case e_qrbinderror:
        dwcError = DWC_ERROR_NETWORK;
        errorCode = DWC_ECODE_TYPE_BIND;
        break;
    case e_qrdnserror:
        dwcError = DWC_ERROR_NETWORK;
        errorCode = DWC_ECODE_TYPE_DNS;
        break;
    case e_qrconnerror:
        dwcError = DWC_ERROR_NETWORK;
        errorCode = DWC_ECODE_TYPE_PEER;
        break;
    case e_qrnochallengeerror:
        dwcError = DWC_ERROR_NETWORK;
        errorCode = DWC_ECODE_TYPE_SERVER;
        break;
    }

    switch (DWC_GetState()) {
    case DWC_STATE_LOGIN:
        errorCode += DWC_ECODE_SEQ_LOGIN + DWC_ECODE_GS_QR2;
        DWCi_StopLogin(dwcError, errorCode);
        break;
    case DWC_STATE_UPDATE_SERVERS:
        errorCode += DWC_ECODE_SEQ_FRIEND + DWC_ECODE_GS_QR2;
        DWCi_StopFriendProcess(dwcError, errorCode);
        break;
    case DWC_STATE_MATCHING:

        errorCode += DWC_ECODE_SEQ_MATCH + DWC_ECODE_GS_QR2;
        DWCi_StopMatching(dwcError, errorCode);
        break;
    default:
        errorCode += DWC_ECODE_SEQ_ETC + DWC_ECODE_GS_QR2;
        DWCi_SetError(dwcError, errorCode);
        break;
    }

    return error;
}
