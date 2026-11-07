#include "context.h"
void native_main_020a2d30 (void)
{
    u32 bitmask;
    int result;
    int i;

    if (!stpOptMinComp || !stpOptMinComp->valid ||
        (DWCi_GetMatchCnt()->qr2MatchType == DWC_MATCH_TYPE_SC_SV) ||
        (DWCi_GetMatchCnt()->qr2MatchType == DWC_MATCH_TYPE_SC_CL))
        return;

    if (DWCi_GetMatchCnt()->state == DWC_MATCH_STATE_SV_POLL_TIMEOUT) {
        bitmask = DWCi_GetAIDBitmask(FALSE);
        if (stpOptMinComp->recvBit == bitmask) {
            if (stpOptMinComp->timeoutBit == bitmask) {
                DWC_Printf(DWC_REPORTFLAG_MATCH_GT2, "[OPT_MIN_COMP] Timeout occured in all hosts.\n");
                DWCi_GetMatchCnt()->qr2NumEntry = (u8)DWCi_GetMatchCnt()->gt2NumConnection;
                DWCi_GetMatchCnt()->clLinkProgress = (u8)(DWCi_GetMatchCnt()->gt2NumConnection - 1);
                DWCi_PostProcessConnection(DWC_PP_CONNECTION_SV_CONNECT);
            } else {
                DWC_Printf(DWC_REPORTFLAG_MATCH_GT2,
                           "[OPT_MIN_COMP] Some clients is in time.\n");

                stpOptMinComp->lastPollTime = OS_GetTick();
                stpOptMinComp->recvBit = 0;

                if (DWCi_GetMatchCnt()->qr2MatchType == DWC_MATCH_TYPE_ANYBODY) {
                    DWCi_SetMatchStatus(DWC_MATCH_STATE_CL_SEARCH_HOST);
                    DWCi_GetMatchCnt()->sbUpdateFlag = DWC_SB_UPDATE_INTERVAL_LONG;
                    DWCi_GetMatchCnt()->sbUpdateTick = OS_GetTick();
                } else {
                    DWCi_SetMatchStatus(DWC_MATCH_STATE_CL_WAIT_RESV);
                    (void)DWCi_SendResvCommandToFriend(TRUE, FALSE, 0);
                }
            }
        } else if (OS_TicksToMilliSeconds(OS_GetTick() - stpOptMinComp->lastPollTime) >= DWC_MATCH_CMD_RTT_TIMEOUT * stpOptMinComp->retry)       {
            DWC_Printf(DWC_REPORTFLAG_DEBUG,
                       "[OPT_MIN_COMP] Timeout: wait poll-ACK %d/%d.\n",
                       stpOptMinComp->retry - 1, DWC_MATCH_OPT_MIN_COMP_POLL_RETRY_MAX);

            if (stpOptMinComp->retry > DWC_MATCH_OPT_MIN_COMP_POLL_RETRY_MAX) {
                DWC_Printf(DWC_REPORTFLAG_DEBUG,
                           "[OPT_MIN_COMP] Timeout: aidbitmap 0x%x. Restart matching.\n",
                           stpOptMinComp->recvBit);

                DWCi_InitOptMinCompParam(TRUE);
                DWCi_CloseAllConnectionsByTimeout();
                DWCi_RestartFromCancel(DWC_MATCH_RESET_RESTART);
            } else {
                for (i = 1; i <= DWCi_GetMatchCnt()->gt2NumConnection; i++) {
                    if (!(stpOptMinComp->recvBit & (1U << DWCi_GetMatchCnt()->aidList[i]))) {
                        result =
                            DWCi_SendMatchCommand(DWC_MATCH_COMMAND_POLL_TIMEOUT,
                                                  DWCi_GetMatchCnt()->sbPidList[i],
                                                  DWCi_GetMatchCnt()->qr2IPList[i],
                                                  DWCi_GetMatchCnt()->qr2PortList[i],
                                                  NULL, 0);
                        if (DWCi_HandleMatchCommandError(result)) return;
                    }
                }
                stpOptMinComp->retry++;
            }
        }
    } else if (((DWCi_GetMatchCnt()->state == DWC_MATCH_STATE_CL_WAIT_RESV) ||
                (DWCi_GetMatchCnt()->state == DWC_MATCH_STATE_CL_SEARCH_HOST)) &&
               (DWCi_GetMatchCnt()->gt2NumConnection >= stpOptMinComp->minEntry - 1) &&
               ((!stpOptMinComp->retry &&
                 (OS_TicksToMilliSeconds(OS_GetTick() - stpOptMinComp->startTime) >= stpOptMinComp->timeout)) ||
                (stpOptMinComp->retry &&
                 (OS_TicksToMilliSeconds(OS_GetTick() - stpOptMinComp->lastPollTime) >= stpOptMinComp->timeout >> 2)))) {

        if (DWCi_GetMatchCnt()->reqProfileID) {
            result = DWCi_CancelReservation(DWCi_GetMatchCnt()->reqProfileID);
            if (DWCi_HandleMatchCommandError(result)) return;
        }

        DWCi_SetMatchStatus(DWC_MATCH_STATE_SV_POLL_TIMEOUT);
        DWC_Printf(DWC_REPORTFLAG_MATCH_GT2,
                   "[OPT_MIN_COMP] Poll timeout (my time is %lu).\n",
                   OS_TicksToMilliSeconds(OS_GetTick() - stpOptMinComp->startTime));

        for (i = 1; i <= DWCi_GetMatchCnt()->gt2NumConnection; i++) {
            result =
                DWCi_SendMatchCommand(DWC_MATCH_COMMAND_POLL_TIMEOUT,
                                      DWCi_GetMatchCnt()->sbPidList[i],
                                      DWCi_GetMatchCnt()->qr2IPList[i],
                                      DWCi_GetMatchCnt()->qr2PortList[i],
                                      NULL, 0);
            if (DWCi_HandleMatchCommandError(result)) return;
        }

        stpOptMinComp->lastPollTime = OS_GetTick();
        stpOptMinComp->retry = 1;
    }
}
