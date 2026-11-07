#include "context.h"
void native_main_0209ef04 (GT2Connection connection,
                                GT2Result result,
                                GT2Byte * message,
                                int len)
{
#pragma unused(len)
    char pidStr[12];
    int index;
    GT2Connection * pGt2Con;
    GT2Result gt2Result;
    DWCConnectionInfo * pConInfo;

    if (!DWCi_GetMatchCnt() ||
        ((DWCi_GetMatchCnt()->state != DWC_MATCH_STATE_CL_GT2) &&
         (DWCi_GetMatchCnt()->state != DWC_MATCH_STATE_SV_OWN_GT2))) {

        DWC_Printf(DWC_REPORTFLAG_MATCH_GT2,
                   "gt2ConnectedCallback: Already cancel\n");
        return;
    }

    if (result != GT2Success) {
        if (!message) message = (GT2Byte *)"";
        DWC_Printf(DWC_REPORTFLAG_MATCH_GT2, "GT2 connect failed %d: %s\n", result, message);

        if (result == GT2DuplicateAddress) {
            return;
        } else if (result == GT2TimedOut)   {
            DWCi_GetMatchCnt()->gt2ConnectCount++;
            if (DWCi_GetMatchCnt()->gt2ConnectCount > DWC_MATCH_CMD_RETRY_MAX) {
                DWC_Printf(DWC_REPORTFLAG_MATCH_GT2, "gt2Connect() retry over.\n");
                DWCi_GetMatchCnt()->gt2ConnectCount = 0;
                DWCi_CancelPreConnectedServerProcess(DWCi_GetMatchCnt()->sbPidList[DWCi_GetMatchCnt()->qr2NNFinishCount]);
                return;
            }

            DWC_Printf(DWC_REPORTFLAG_MATCH_GT2, "Retry to gt2Connect.\n");

            (void)OS_SNPrintf(pidStr, sizeof(pidStr), native_data_020e01a4, DWCi_GetMatchCnt()->profileID);
            gt2Result =
                gt2Connect(*DWCi_GetMatchCnt()->pGt2Socket,
                           NULL,
                           gt2AddressToString(
                               DWCi_GetMatchCnt()->ipList[DWCi_GetMatchCnt()->qr2NNFinishCount],
                               DWCi_GetMatchCnt()->portList[DWCi_GetMatchCnt()->qr2NNFinishCount],
                               NULL),
                           (GT2Byte *)pidStr,
                           -1,
                           DWC_GT2_CONNECT_TIMEOUT,
                           DWCi_GetMatchCnt()->gt2Callbacks,
                           GT2False);
            if (gt2Result == GT2OutOfMemory) {
                DWCi_HandleGT2Error(gt2Result);
                return;
            } else if (gt2Result == GT2Success)   {

            } else if (!DWCi_CancelPreConnectedServerProcess(DWCi_GetMatchCnt()->sbPidList[DWCi_GetMatchCnt()->qr2NNFinishCount]))   {
                return;
            }
        } else {
            if (!DWCi_CancelPreConnectedServerProcess(DWCi_GetMatchCnt()->sbPidList[DWCi_GetMatchCnt()->gt2NumConnection + 1]))
                return;
        }
    } else {
        DWC_Printf(DWC_REPORTFLAG_MATCH_GT2, "GT2 connected.\n");
        index = DWCi_GT2GetConnectionListIdx();

        if (index == -1) {
            DWC_Printf(DWC_REPORTFLAG_WARNING,
                       "Don't continue matching without closing connections!!\n");

            DWCi_StopMatching(DWC_ERROR_NETWORK,
                              DWC_ECODE_SEQ_MATCH + DWC_ECODE_GS_GT2 + DWC_ECODE_TYPE_CONN_OVER);
            return;
        }

        pGt2Con = DWCi_GetGT2ConnectionByIdx(index);
        pConInfo = DWCi_GetConnectionInfoByIdx(index);

        *pGt2Con = connection;
        DWCi_GetMatchCnt()->gt2NumConnection++;

        pConInfo->index = (u8)index;
        pConInfo->reserve = 0;
        pConInfo->param = NULL;
        pConInfo->aid = DWCi_GetMatchCnt()->aidList[DWCi_GetMatchCnt()->gt2NumConnection];

        gt2SetConnectionData(connection, pConInfo);

        if (DWCi_GetMatchCnt()->state == DWC_MATCH_STATE_SV_OWN_GT2) {
            DWCi_PostProcessConnection(DWC_PP_CONNECTION_SV_CONNECT);
        } else {
            DWCi_PostProcessConnection(DWC_PP_CONNECTION_CL_GT2_CONNECT);
        }
    }
}
