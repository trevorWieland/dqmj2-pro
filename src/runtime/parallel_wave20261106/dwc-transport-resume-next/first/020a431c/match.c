#include "context.h"
void native_main_020a431c (u8 aid)
{
    if (!sTransInfo) return;

    sTransInfo->connections[aid].sendingSize = 0;
    sTransInfo->connections[aid].recvingSize = 0;
    sTransInfo->connections[aid].requestSendSize = 0;
    sTransInfo->connections[aid].requestRecvSize = 0;
    sTransInfo->connections[aid].sendState = 0;

    sTransInfo->connections[aid].recvBuffer = NULL;
    sTransInfo->connections[aid].recvBufferSize = 0;
    sTransInfo->connections[aid].recvState = DWC_TRANSPORT_RECV_NOBUF;

    sTransInfo->connections[aid].lastRecvType = 0;
}
