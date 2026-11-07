#include "context.h"
void native_main_020a44f4 (u8 aid, DWCTransportHeader * message, int size)
{
    u16 type;
    DWCTransportConnection * connection = &sTransInfo->connections[aid];
    DWCTransportHeader header;

    connection->lastRecvState = (u8)DWCs_GetRecvState(aid);

    switch (type = DWCs_DecodeHeader(message)) {
    case DWC_SEND_TYPE_USERDATA:
        if (size != sizeof(DWCTransportHeader)) {
            DWC_Printf(DWC_REPORTFLAG_RECV_INFO, "+++ Invalid header from aid %d\n", aid);
            return;
        }

        MI_CpuCopy8(message, &header, sizeof(DWCTransportHeader));

        connection->requestRecvSize = header.size;
        connection->recvingSize = 0;

        if (connection->recvBuffer &&
            connection->recvBufferSize >= connection->requestRecvSize) {
            connection->recvState = DWC_TRANSPORT_RECV_BODY;
        } else {
            connection->recvState = DWC_TRANSPORT_RECV_ERROR;
        }
        break;
    case DWC_SEND_TYPE_MATCH_SYN:
    case DWC_SEND_TYPE_MATCH_SYN_ACK:
    case DWC_SEND_TYPE_MATCH_ACK:
        DWC_Printf(DWC_REPORTFLAG_RECV_INFO, "Received system header.\n");
        connection->recvState = DWC_TRANSPORT_RECV_SYSTEM_DATA;
        break;
    default:
        DWC_Printf(DWC_REPORTFLAG_RECV_INFO, "+++ Invalid header from aid %d\n", aid);
        break;
    }

    connection->lastRecvType = type;
}
