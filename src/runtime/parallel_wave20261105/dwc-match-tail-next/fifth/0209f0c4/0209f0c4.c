#include "context.h"
void native_main_0209f0c4 (GPConnection * pconnection, int profileID, char * message)
{
#pragma unused(pconnection)
    char tmpStr[16];
    u32 data[DWC_MATCH_COMMAND_ADD_MESSAGE_NUM];
    int i;
    DWC_Printf(DWC_REPORTFLAG_MATCH_NN,
               "<GP> RECV-0x%02x <- [--------:-----] [pid=%u]\n",
               *message, profileID);
    for (i = 0; i < DWC_MATCH_COMMAND_ADD_MESSAGE_NUM; i++) {
        if (native_fn_020a0330(tmpStr, message + 1, i) == -1) break;
        data[i] = strtoul(tmpStr, NULL, 10);
    }
    (void)native_fn_020a039c((u8) * message, profileID, 0, 0, data, i);
}
