#include "context.h"
DWCError native_main_0209a944 (int * errorCode, DWCErrorType * errorType)
{
    if (errorCode != NULL) *errorCode = stDwcErrorCode;
    if (errorType != NULL) {
        switch (stDwcLastError) {
        case DWC_ERROR_AUTH_ANY:
        case DWC_ERROR_AUTH_OUT_OF_SERVICE:
        case DWC_ERROR_AUTH_STOP_SERVICE:
        case DWC_ERROR_AC_ANY:
        case DWC_ERROR_DISCONNECTED:
            *errorType = DWC_ETYPE_DISCONNECT;
            break;
        case DWC_ERROR_NETWORK:
            *errorType = DWC_ETYPE_SHUTDOWN_FM;
            break;
        case DWC_ERROR_GHTTP_ANY:
            *errorType = DWC_ETYPE_SHUTDOWN_GHTTP;
            break;
        case DWC_ERROR_FRIENDS_SHORTAGE:
        case DWC_ERROR_NOT_FRIEND_SERVER:
        case DWC_ERROR_MO_SC_CONNECT_BLOCK:
        case DWC_ERROR_SERVER_FULL:
            *errorType = DWC_ETYPE_LIGHT;
            break;
        case DWC_ERROR_DS_MEMORY_ANY:
        case DWC_ERROR_FATAL:
            *errorType = DWC_ETYPE_FATAL;
            break;
        case DWC_ERROR_ND_ANY:
            *errorType = DWC_ETYPE_SHUTDOWN_ND;
            break;
        case DWC_ERROR_ND_HTTP:
        case DWC_ERROR_SVL_HTTP:
        case DWC_ERROR_PROF_HTTP:
            *errorType = DWC_ETYPE_DISCONNECT;
            break;
        case 20:
        case 21:
        case DWC_ERROR_SVL_ANY:
        case DWC_ERROR_PROF_ANY:
            *errorType = DWC_ETYPE_SHOW_ERROR;
            break;
        case DWC_ERROR_NONE:
        default:
            *errorType = DWC_ETYPE_NO_ERROR;
            break;
        }
    }
    return stDwcLastError;
}
