#include "context.h"
void native_main_020a4404 (GT2Connection connection, u8 * message, int size)
{
    u8 aid = DWCi_GetConnectionAID(connection);
    u16 type;

    switch (DWCs_GetRecvState(aid)) {
    case DWC_TRANSPORT_RECV_NOBUF:
        type = DWCs_DecodeHeader((DWCTransportHeader *) message);
        if (type >= DWC_SEND_TYPE_MATCH_SYN &&
            type <= DWC_SEND_TYPE_MATCH_ACK) {
            DWCs_RecvDataHeader(aid, (DWCTransportHeader *) message, size);
        } else {
            DWC_Printf(DWC_REPORTFLAG_RECV_INFO, "+++ Recv buffer is not set\n");
        }
        break;
    case DWC_TRANSPORT_RECV_HEADER:
        DWCs_RecvDataHeader(aid, (DWCTransportHeader *) message, size);
        break;
    case DWC_TRANSPORT_RECV_BODY:
        DWCs_RecvDataBody(aid, message, size);
        break;
    case DWC_TRANSPORT_RECV_SYSTEM_DATA:
        DWCs_RecvSystemDataBody (aid, message, size);
        break;
    case DWC_TRANSPORT_RECV_ERROR:
        DWC_Printf(DWC_REPORTFLAG_RECV_INFO, "+++ Recv size is too large ( buffer size = %d < %d )\n", sTransInfo->connections[aid].recvBufferSize, size);

        sTransInfo->connections[aid].recvState = DWC_TRANSPORT_RECV_HEADER;
        sTransInfo->connections[aid].recvingSize = 0;
        sTransInfo->connections[aid].requestRecvSize = 0;
        break;
    default:
        DWC_Printf(DWC_REPORTFLAG_ERROR, "Recv error (state is %d).\n", DWCs_GetRecvState(aid));
        DWCi_SetError(DWC_ERROR_NETWORK, DWC_ECODE_SEQ_ETC + DWC_ECODE_GS_GT2 + DWC_ECODE_TYPE_TRANS_HEADER);
        break;
    }
}
