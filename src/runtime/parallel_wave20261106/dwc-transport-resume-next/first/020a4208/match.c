#include "context.h"
void native_main_020a4208 (void)
{
    u8 * aidList;
    s32 hostCount;
    s32 i;

    if (!sTransInfo) {
        return;
    }

    hostCount = DWC_GetAIDList(&aidList);

    for (i = 0; i < hostCount ; i++) {
        u8 aid;
        aid = aidList[i];
        native_fn_020a3df0();

        if (DWC_IsValidAID(aid)) {
            DWCTransportConnection * transConnection;
            transConnection = DWCs_GetTransConnection(aid);

            if (sTransInfo->recvTimeoutCallback && (transConnection->recvTimeoutTime > 0)) {
                u32 time;
                OSTick currentTick;

                currentTick = OS_GetTick();
                time = (u32)OS_TicksToMilliSeconds(currentTick - transConnection->previousRecvTick);
                if (time > transConnection->recvTimeoutTime) {
                    DWC_Printf(DWC_REPORTFLAG_RECV_INFO, "DWCi_TransportProcess:timeout aid=%d,time=%d[ms],timeout time=%d[ms]\n", aid, time, transConnection->recvTimeoutTime);
                    sTransInfo->recvTimeoutCallback(aid);

                    transConnection->previousRecvTick = currentTick;
                }
            }
        }

        if (aid != DWC_GetMyAID() && DWCs_GetSendState(aid) == DWC_TRANSPORT_SEND_BUSY) {
            s32 restSize;
            s32 sendSize;
            s32 freeSpace;
            DWCTransportConnection * transConnection;

            transConnection = DWCs_GetTransConnection(aid);
            restSize = transConnection->requestSendSize - transConnection->sendingSize;

            if (restSize > sTransInfo->sendSplitMax) {
                sendSize = sTransInfo->sendSplitMax;
            } else {
                sendSize = restSize;
            }

            freeSpace = DWCs_GetOutgoingBufferFreeSize(aid);
            if (freeSpace < sendSize) {
                DWC_Printf(DWC_REPORTFLAG_SEND_INFO, "DWCi_TransportProcess:freeSpace < sendSize:aid:%d, %d < %d\n", aid, freeSpace, sendSize);
                continue;
            }

            DWCs_Send(aid, (u8 *) transConnection->sendBuffer + transConnection->sendingSize, sendSize, TRUE);

            transConnection->sendingSize += sendSize;

            DWC_Printf(
                DWC_REPORTFLAG_SEND_INFO,
                "DWCi_TransportProcess:aid = %d, size = %d/%d, outgoing buffer = %d, vcont = %d\n",
                aid, transConnection->sendingSize, transConnection->requestSendSize, freeSpace - sendSize, OS_GetVBlankCount()
            );

            if (transConnection->sendingSize == transConnection->requestSendSize) {
                int reqSendSize = transConnection->requestSendSize;

                transConnection->sendState = DWC_TRANSPORT_SEND_READY;
                transConnection->sendBuffer = NULL;
                transConnection->sendingSize = 0;
                transConnection->requestSendSize = 0;

                if (sTransInfo->sendCallback) {
                    sTransInfo->sendCallback(reqSendSize, aid);
                }
            }
        }
    }

#ifndef SDK_FINALROM
    {
        OSTick now = OS_GetTick();
        DWCs_DelayCheck(sTransInfo->delayedSend, now, TRUE);
        DWCs_DelayCheck(sTransInfo->delayedRecv, now, FALSE);
    }
#endif
}
