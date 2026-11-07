#include "context.h"
void native_main_020a45fc (u8 aid, void * message, int size)
{
#pragma unused(size)
    DWCTransportConnection * transConnection = DWCs_GetTransConnection(aid);

    transConnection->recvState = transConnection->lastRecvState;

    switch (transConnection->lastRecvType) {
    case DWC_SEND_TYPE_MATCH_SYN:
    case DWC_SEND_TYPE_MATCH_SYN_ACK:
    case DWC_SEND_TYPE_MATCH_ACK:
        DWCi_ProcessMatchSynPacket(aid, transConnection->lastRecvType, (u8 *)message);
        break;
    }
}
