#include "context.h"
SBError native_main_020a020c (u8 command, u32 ip, u16 port, const u32 data[], int len)
{
    int i;
    DWCSBMessage senddata;
    SBError sbError;
    if (len > sizeof(senddata.data) / sizeof(u32)) {
        SDK_ASSERTMSG(0, "Match command is too long.");
        len = sizeof(senddata.data) / sizeof(u32);
    }
    if (data && len) {
        native_fn_02008c28(data, senddata.data, sizeof(u32) * len);
    } else {
        len = 0;
    }
    memcpy(senddata.header.identifier, DWC_SB_COMMAND_STRING, 5);
    senddata.header.version = DWC_MATCHING_VERSION;
    senddata.header.command = command;
    senddata.header.size = (u8)(sizeof(u32) * len);
    senddata.header.qr2Port = native_fn_020a3d70()->qr2Port;
    senddata.header.qr2IP = native_fn_020a3d70()->qr2IP;
    senddata.header.profileID = native_fn_020a3d70()->profileID;
#ifdef NITRODWC_DEBUG
    DWC_Printf(DWC_REPORTFLAG_MATCH_NN,
               "<SB> SEND-%s -> [%08x:%d] [pid=--------]\n",
               get_dwccommandstr(command), ip, port);
#else
    DWC_Printf(DWC_REPORTFLAG_MATCH_NN,
               "<SB> SEND-0x%02x -> [%08x:%d] [pid=--------]\n",
               command, ip, port);
#endif
    for (i = 0; i < DWC_DNS_ERROR_RETRY_MAX; i++) {
        sbError =
            native_fn_020a68b4(native_fn_020a3d70()->sbObj,
                                             native_fn_020b5f38(ip, 0, NULL),
                                             port,
                                             (gsi_char *)&senddata,
                                             (int)(sizeof(DWCSBMessageHeader) + senddata.header.size));
        if (!sbError) break;
        else if (sbError != sbe_dnserror) break;
    }
    return sbError;
}
