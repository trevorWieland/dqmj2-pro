#include "context.h"
BOOL native_main_020a2724 (int profileID, u8 command)
{
    u32 senddata;
    int len;
    int result;
    DWC_Printf(DWC_REPORTFLAG_MATCH_GT2, "Sent CANCEL SYN %d command to %u.\n",
               command - DWC_MATCH_COMMAND_CANCEL_SYN, profileID);
    if (command == DWC_MATCH_COMMAND_CANCEL_SYN) {
        senddata = (u32)native_fn_020a3d70()->cbEventPid;
        len = 1;
    } else {
        len = 0;
    }
    result = native_fn_020a00ac(command, profileID, 0, 0, &senddata, len);
    if (native_fn_020a1258(result)) return FALSE;
    native_fn_020a3d70()->lastCancelSynSent = native_fn_02007a9c();
    return TRUE;
}
