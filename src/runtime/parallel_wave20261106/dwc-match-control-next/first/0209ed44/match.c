#include "context.h"
void native_main_0209ed44 (GT2Socket socket,
                                     GT2Connection connection,
                                     unsigned int ip,
                                     unsigned short port,
                                     int latency,
                                     GT2Byte * message,
                                     int len)
{
#pragma unused(socket)
#pragma unused(message)
#pragma unused(len)
    int index;
    GT2Bool result;
    GT2Connection * pGt2Con;
    DWCConnectionInfo * pConInfo;

    if (!DWCi_GetMatchCnt() || (DWCi_GetMatchCnt()->state != DWC_MATCH_STATE_CL_GT2) ||
        (DWCi_GetMatchCnt()->cancelState != DWC_MATCH_CANCEL_STATE_INIT)) {
        gt2Reject(connection, (const GT2Byte *)native_data_020e01bc, -1);
        DWC_Printf(DWC_REPORTFLAG_MATCH_GT2, "gt2Reject was called : Init state\n");
        return;
    }

    index = DWCi_GT2GetConnectionListIdx();
    if (index == -1) {
        gt2Reject(connection, (const GT2Byte *)native_data_020e01c8, -1);
        DWC_Printf(DWC_REPORTFLAG_MATCH_GT2, "gt2Reject was called : Server full\n");
        DWCi_StopMatching(DWC_ERROR_NETWORK,
                          DWC_ECODE_SEQ_MATCH + DWC_ECODE_GS_GT2 + DWC_ECODE_TYPE_CONN_OVER);
    } else {
        if ((ip != DWCi_GetMatchCnt()->ipList[DWCi_GetMatchCnt()->gt2NumConnection]) ||
            (port != DWCi_GetMatchCnt()->portList[DWCi_GetMatchCnt()->gt2NumConnection])) {
            if (message[0] &&
                (strtoul((const char *)message, NULL, 10) == DWCi_GetMatchCnt()->sbPidList[DWCi_GetMatchCnt()->gt2NumConnection])) {

                DWC_Printf(DWC_REPORTFLAG_WARNING,
                           "gt2Connect() came before NN complete.\n");

                DWCi_GetMatchCnt()->ipList[DWCi_GetMatchCnt()->gt2NumConnection] = ip;
                DWCi_GetMatchCnt()->portList[DWCi_GetMatchCnt()->gt2NumConnection] = port;
            } else {
                gt2Reject(connection, (const GT2Byte *)native_data_020e01d4, -1);
                DWC_Printf(DWC_REPORTFLAG_WARNING,
                           "gt2Reject was called : Unknown connect attempt from %s\n",
                           gt2AddressToString(ip, port, NULL));
                return;
            }
        }

        DWCi_GetMatchCnt()->nnFinishTime = 0;

        result = gt2Accept(connection, DWCi_GetMatchCnt()->gt2Callbacks);
        if (result == GT2False) {
            DWC_Printf(DWC_REPORTFLAG_WARNING, "Unexpected failure to gt2Accept.\n");
            DWCi_StopMatching(DWC_ERROR_NETWORK,
                              DWC_ECODE_SEQ_MATCH + DWC_ECODE_TYPE_OTHER);
            return;
        }

        DWC_Printf(DWC_REPORTFLAG_MATCH_GT2,
                   "Accepted connection from %s (latency %d)\n",
                   gt2AddressToString(ip, port, NULL), latency);

        DWCi_StopResendingMatchCommand();

        if (DWCi_GetMatchCnt()->gt2NumConnection == 0) {
            DWCi_GetMatchCnt()->baseLatency =
                (u16)(((latency >> 1) < 0xffff) ? (latency >> 1) : 0xffff);
        }

        pGt2Con = DWCi_GetGT2ConnectionByIdx(index);
        pConInfo = DWCi_GetConnectionInfoByIdx(index);
        *pGt2Con = connection;

        DWCi_GetMatchCnt()->gt2NumConnection++;

        pConInfo->index = (u8)index;
        pConInfo->aid = DWCi_GetMatchCnt()->aidList[DWCi_GetMatchCnt()->gt2NumConnection - 1];
        pConInfo->reserve = 0;
        pConInfo->param = NULL;

        gt2SetConnectionData(connection, pConInfo);
        DWCi_PostProcessConnection(DWC_PP_CONNECTION_CL_GT2_ACCEPT);
    }
}
