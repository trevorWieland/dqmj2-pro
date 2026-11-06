#include "context.h"
void native_main_0209c188 (GPConnection * pconnection, GPRecvBuddyMessageArg * arg, void * param)
{
#pragma unused(param)
    char version[12] = { 0, };
    char * message = arg->message;
    u32 len;


    if (memcmp(message, DWC_GP_COMMAND_STRING, strlen(DWC_GP_COMMAND_STRING))) {
        DWC_Printf(DWC_REPORTFLAG_WARNING,
                   "Received undefined buddy message. '%s'\n",
                   message);
        return;
    }

    message += strlen(DWC_GP_COMMAND_STRING);
    len = (u32)(strchr(message, 'v') - message);
    strncpy(version, message, len);
    if ((len > 10) || (strtoul(version, NULL, 10) != DWC_MATCHING_VERSION)) {

        DWC_Printf(DWC_REPORTFLAG_WARNING,
                   "Received different version buddy message command. '%s'\n",
                   message);
        return;
    }

    message += len + 1;
    if (memcmp(message, DWC_GP_COMMAND_MATCH_STRING, strlen(DWC_GP_COMMAND_MATCH_STRING)) == 0) {

        if ((stpDwcCnt->state == DWC_STATE_MATCHING) ||
            ((stpDwcCnt->state == DWC_STATE_CONNECTED) &&
             ((stpDwcCnt->matchcnt.qr2MatchType == DWC_MATCH_TYPE_SC_SV) ||
              (stpDwcCnt->matchcnt.qr2MatchType == DWC_MATCH_TYPE_SC_CL)))) {
            message += strlen(DWC_GP_COMMAND_MATCH_STRING);
            DWCi_MatchGPRecvBuddyMsgCallback(pconnection, arg->profile, message);
        } else {
            DWC_Printf(DWC_REPORTFLAG_DEBUG, "Ignore delayed GP matching command.\n");
        }
    }
}