#include "context.h"
GPResult native_main_020a02b4 (GPConnection * connection, u8 command, int profileID, const char * message)
{
    char tmpStr[DWC_MATCH_COMMAND_ADD_MESSAGE_MAX];
    u32 len, len2;
    char *out;
    GPResult result;
    len = (u32)native_fn_020061ac(tmpStr, sizeof(tmpStr),
                           native_data_020e02a4,
                           DWC_GP_COMMAND_STRING,
                           DWC_MATCHING_VERSION,
                           DWC_GP_COMMAND_MATCH_STRING);
    tmpStr[len] = (char)command;
    out=(tmpStr+1)+len;
    *out=0;
    if (message) {
        len2 = strlen(message);
        if ((len + 1) + len2 + 1 > sizeof(tmpStr)) {
            SDK_ASSERTMSG(0, "Match command is too long.");
            len2 = sizeof(tmpStr) - (len + 1) - 1;
        }
        native_fn_02008e0c(message, out, len2);
        out[len2]=0;
    }
    result = native_fn_020aa7c0(connection, profileID, tmpStr);
    DWC_Printf(DWC_REPORTFLAG_MATCH_NN,
               "<GP> SEND-0x%02x -> [--------:-----] [pid=%u]\n",
               command, profileID);
    return result;
}
