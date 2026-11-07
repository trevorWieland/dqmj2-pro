#include "context.h"
void native_main_020a449c (GT2Connection connection, void * message, int size)
{
    u8 aid = DWCi_GetConnectionAID(connection);
    DWCTransportConnection * transConnection = &sTransInfo->connections[aid];

    if (transConnection->recvBuffer &&
        transConnection->recvBufferSize >= size) {

        if (sTransInfo->recvCallback) {
            sTransInfo->recvCallback(aid, message, size);
        }

        if (sTransInfo->recvTimeoutCallback && (transConnection->recvTimeoutTime > 0)) {
            transConnection->previousRecvTick = OS_GetTick();
        }
    } else {
        DWC_Printf(DWC_REPORTFLAG_RECV_INFO, "Recv data size is too large (%d > %d)\n", size, transConnection->recvBufferSize);
        return;
    }
}
