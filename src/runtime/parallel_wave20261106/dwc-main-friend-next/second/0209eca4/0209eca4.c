#include "context.h"
GT2Bool native_main_0209eca4 (GT2Socket socket,
                                             unsigned int ip,
                                             unsigned short port,
                                             GT2Byte * message,
                                             int len)
{
#pragma unused(socket)
    struct sockaddr_in saddr;

    if (!len || !message) return GT2False;

    MI_CpuClear32(&saddr, sizeof(saddr));

    saddr.sin_family = AF_INET;
    saddr.sin_addr.s_addr = ip;
    saddr.sin_port = htons(port);

    if (((message[0] == QR_MAGIC_1) && (message[1] == QR_MAGIC_2))
        || (message[0] == '\\')) {

        DWC_Printf(DWC_REPORTFLAG_MATCH_NN, "GT2 Unrecognized : Received QR2 data.\n");

        if (DWCi_GetMatchCnt()->qr2Obj) {
            qr2_parse_query(DWCi_GetMatchCnt()->qr2Obj, (gsi_char *)message, len, (struct sockaddr *)&saddr);
        } else {
            DWC_Printf(DWC_REPORTFLAG_MATCH_NN, "  ignore qr2 message.\n");
        }
    } else if (!memcmp(message, NNMagicData, NATNEG_MAGIC_LEN))   {
        DWC_Printf(DWC_REPORTFLAG_MATCH_NN, "GT2 Unrecognized : Received NN data.\n");
        NNProcessData((char *)message, len, &saddr);
    } else if ((message[0] == 0xfe) && (message[1] == 0xfe))   {
        DWC_Printf(DWC_REPORTFLAG_MATCH_GT2, "GT2 Unrecognized : Not Connected gt2 data.\n");
        return GT2False;
    } else {
        DWC_Printf(DWC_REPORTFLAG_WARNING, "GT2 Unrecognized : Received unrecognized data.\n");
        return GT2False;
    }

    return GT2True;
}
