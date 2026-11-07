#include "context.h"
void native_main_020a456c (u8 aid, void * message, int size)
{
    DWCTransportConnection * connection;
    int requestSize;

    connection = &sTransInfo->connections[aid];

    if (DWCs_GetRecvState(aid) == DWC_TRANSPORT_RECV_BODY) {
        if (connection->recvingSize + size > connection->recvBufferSize) {
            DWC_Printf(DWC_REPORTFLAG_ERROR, "Recv buffer over flow.\n");
            DWCi_SetError(DWC_ERROR_NETWORK, DWC_ECODE_SEQ_ETC + DWC_ECODE_GS_GT2 + DWC_ECODE_TYPE_TRANS_BODY);
            return;
        }

        MI_CpuCopy8(message, (u8 *)connection->recvBuffer + connection->recvingSize, (u32) size);
    }

    connection->recvingSize += size;

    DWC_Printf(DWC_REPORTFLAG_RECV_INFO, "aid = %d size = %d/%d state = %d incoming buffer = %d\n",
               aid,
               connection->recvingSize, connection->requestRecvSize,
               DWCs_GetRecvState(aid),
               gt2GetIncomingBufferFreeSpace(DWCi_GetGT2Connection(aid)));

    if (connection->recvingSize == connection->requestRecvSize) {
        requestSize = connection->requestRecvSize;
        connection->recvState = DWC_TRANSPORT_RECV_HEADER;
        connection->recvingSize = 0;
        connection->requestRecvSize = 0;

        if (sTransInfo->recvCallback) {
            sTransInfo->recvCallback(aid, connection->recvBuffer, requestSize);
        }
    }

    if (sTransInfo->recvTimeoutCallback && (connection->recvTimeoutTime > 0)) {
        connection->previousRecvTick = OS_GetTick();
    }
}
