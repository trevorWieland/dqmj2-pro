#include "context.h"
BOOL native_main_020a3f84 (u16 type, u8 aid, const void * buffer, int size)
{
    DWCTransportConnection * transConnection = DWCs_GetTransConnection(aid);
    DWCTransportHeader header;
    int sendSize;
    int freeSpace;

    SDK_ASSERT(buffer);
    SDK_ASSERT(size > 0);

    if (!DWCi_IsSendableReliable(aid, type)) {
        return FALSE;
    }

    transConnection->sendState = DWC_TRANSPORT_SEND_BUSY;
    transConnection->sendBuffer = buffer;
    transConnection->sendingSize = 0;
    transConnection->requestSendSize = size;

    DWCs_EncodeHeader(&header, type, size);
    DWCs_Send(aid, (const u8 *) &header, sizeof(DWCTransportHeader), TRUE);

    if (size > sTransInfo->sendSplitMax) {
        sendSize = sTransInfo->sendSplitMax;
    } else {
        sendSize = size;
    }

    freeSpace = DWCs_GetOutgoingBufferFreeSize(aid);

    DWC_Printf(
        DWC_REPORTFLAG_SEND_INFO,
        "DWCi_SendReliable:aid = %d,%d,%d,%d,%d,vcount = %d\n",
        aid, sendSize, freeSpace, size, sTransInfo->sendSplitMax, OS_GetVBlankCount()
    );

    if (sendSize > freeSpace) {
        DWC_Printf(
            DWC_REPORTFLAG_SEND_INFO,
            "DWCi_SendReliable:sendSize > freeSpace:aid = %d,%d,%d,vcount = %d\n",
            aid, sendSize, freeSpace, OS_GetVBlankCount()
        );
        return TRUE;
    }

    DWCs_Send(aid, buffer, sendSize, TRUE);

    transConnection->sendingSize += sendSize;

    DWC_Printf(
        DWC_REPORTFLAG_SEND_INFO,
        "[R] aid = %d, size = %d/%d, outgoing buffer = %d, vcount = %d\n",
        aid, transConnection->sendingSize, transConnection->requestSendSize, freeSpace - sendSize, OS_GetVBlankCount()
    );

    if (transConnection->sendingSize == transConnection->requestSendSize) {
        int reqSendSize = transConnection->requestSendSize;

        transConnection->sendState = DWC_TRANSPORT_SEND_READY;
        transConnection->sendBuffer = NULL;
        transConnection->sendingSize = 0;
        transConnection->requestSendSize = 0;

        if (sTransInfo->sendCallback && type == DWC_SEND_TYPE_USERDATA) {
            sTransInfo->sendCallback(reqSendSize, aid);
        }
    }

    return TRUE;
}
