#include "context.h"
GT2Result native_main_0209bf8c (GT2Result result)
{
    int errorCode;
    DWCError dwcError;

    if (result == GT2Success) return GT2Success;

    DWC_Printf(DWC_REPORTFLAG_ERROR, "Main, GT2 error %d\n", result);

    switch (result) {
    case GT2OutOfMemory:
        dwcError = DWC_ERROR_FATAL;
        errorCode = DWC_ECODE_TYPE_ALLOC;
        break;
    case GT2Rejected:
    case GT2DuplicateAddress:
        dwcError = DWC_ERROR_NONE;
        errorCode = 0;
        result = GT2Success;
        break;
    case GT2NetworkError:
        dwcError = DWC_ERROR_NETWORK;
        errorCode = DWC_ECODE_TYPE_NETWORK;
        break;
    case GT2AddressError:
        dwcError = DWC_ERROR_NETWORK;
        errorCode = DWC_ECODE_TYPE_DNS;
        break;
    case GT2TimedOut:
        dwcError = DWC_ERROR_NETWORK;
        errorCode = DWC_ECODE_TYPE_TIMEOUT;
        break;
    case GT2NegotiationError:
        dwcError = DWC_ERROR_NETWORK;
        errorCode = DWC_ECODE_TYPE_PEER;
        break;
    }

    if (dwcError) {
        errorCode += DWC_ECODE_SEQ_LOGIN + DWC_ECODE_GS_GT2;
        DWCi_StopLogin(dwcError, errorCode);
    }

    return result;
}