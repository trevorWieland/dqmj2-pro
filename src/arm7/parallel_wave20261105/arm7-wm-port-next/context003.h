void native_host_arm7_main_027e7828(u16 aidBitmap)
{
    WMSPWork *sys = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    WMPortSendQueueData *queueData = status->sendQueueData;
    int iQueue;
    int iPrio;
    u32 aidBitmapMask;
    u32 childBitmap;
    ((void)0) ;
    childBitmap = status->child_bitmap;
    aidBitmapMask = (~aidBitmap) & childBitmap;
    native_host_arm7_arm_037fc888(&status->sendQueueMutex);
    for (iQueue = 0; iQueue < 2; iQueue++) {
        WMPortSendQueue *baseQueue;
        baseQueue = (iQueue == 0) ? status->sendQueue : status->readyQueue;
        baseQueue = status->readyQueue;
        for (iPrio = 0; iPrio < 4 ; iPrio++) {
            WMPortSendQueue *queue;
            u32 index;
            u16 *prevPointer;
            u32 prevIndex;
            queue = &baseQueue[iPrio];
            prevPointer = &queue->head;
            prevIndex = ((u16)0xffff) ;
            for (index = queue->head; index != ((u16)0xffff) ;
                index = (u32)((index != ((u16)0xffff) ) ? queueData[index].next : queue->head)) {
                WMPortSendQueueData *data = &queueData[index];
                if ((data->restBitmap & ~childBitmap) != 0) {
                    ((void)0)
                        ;
                }
                data->restBitmap &= aidBitmapMask;
                data->sendingBitmap &= aidBitmapMask;
                if (data->restBitmap == 0) {
                    WMPortSendCallback *cb_PortSend;
                    cb_PortSend = (WMPortSendCallback *)native_host_arm7_arm_038073f0();
                    cb_PortSend->apiid = WM_APIID_PORT_SEND;
                    cb_PortSend->errcode = WM_ERRCODE_SUCCESS;
                    cb_PortSend->state = WM_STATECODE_PORT_SEND;
                    cb_PortSend->port = data->port;
                    cb_PortSend->destBitmap = data->destBitmap;
                    cb_PortSend->restBitmap = data->restBitmap;
                    cb_PortSend->sentBitmap = data->sentBitmap;
                    cb_PortSend->size = data->size;
                    cb_PortSend->data = data->data;
                    cb_PortSend->callback = data->callback;
                    cb_PortSend->arg = data->arg;
                    cb_PortSend->seqNo = data->seqNo;
                    {
                        u16 parentSize = status->mp_parentSize;
                        u16 childSize = status->mp_childSize;
                        cb_PortSend->maxSendDataSize = (status->aid == 0) ? parentSize : childSize;
                        cb_PortSend->maxRecvDataSize = (status->aid == 0) ? childSize : parentSize;
                    }
                    native_host_arm7_arm_038073a4(cb_PortSend);
                    if (data->next == ((u16)0xffff) ) {
                        queue->tail = (u16)prevIndex;
                    }
                    *prevPointer = data->next;
                    data->next = ((u16)0xffff) ;
                    if (status->sendQueueFreeList.tail == ((u16)0xffff) ) {
                        status->sendQueueFreeList.head = (u16)index;
                    } else {
                        queueData[status->sendQueueFreeList.tail].next = (u16)index;
                    }
                    status->sendQueueFreeList.tail = (u16)index;
                    index = prevIndex;
                }
                if (index != ((u16)0xffff) ) {
                    prevPointer = &(queueData[index].next);
                } else {
                    prevPointer = &queue->head;
                }
                prevIndex = index;
            }
        }
    }
    native_host_arm7_arm_037fc90c(&status->sendQueueMutex);
    return;
}

void native_host_arm7_main_027e7a1c(u16 aid, u16 wmHeader, u16 *data, u16 length, WMMpRecvBuf *recvBuf)
{
    WMStatus *status = WMSP_GetStatusStructure();
    int restSize = length;
    BOOL firstPacketFlag;
    ((void)0) ;
    if (length == 0) {
        ((void)0) ;
        return;
    }
    if (length > 0x204) {
        ((void)0) ;
        return;
    }
    if (aid == status->aid || aid >= (15 + 1)) {
        ((void)0) ;
        return;
    }
    if (length & 1 == 1) {
        ((void)0) ;
        return;
    }
    firstPacketFlag = 1 ;
    while (restSize > 0) {
        int len, packetLength;
        BOOL destBmpFlag, seqNoFlag;
        u16 *header;
        u16 *footer;
        u16 *contents;
        u32 port;
        u32 seqNo = 0xffffU;
        if (firstPacketFlag == 1 ) {
            firstPacketFlag = 0 ;
            header = &wmHeader;
        } else {
            header = data;
            data++;
            restSize -= 2 ;
        }
        len = (*header & 0x00ff ) * 2 ;
        if (len == 0) {
            len = (0x00ff + 1) * 2 ;
        }
        destBmpFlag = (*header & 0x1000 ) ? 1 : 0 ;
        seqNoFlag = (*header & 0x0800 ) ? 1 : 0 ;
        packetLength = len + (seqNoFlag ? 2 : 0) + (destBmpFlag ? 2 : 0);
        restSize -= packetLength;
        if (restSize < 0) {
            ((void)0) ;
            break;
        }
        port = ((u16)(((*header) & 0x0f00 ) >> 8 ));
        contents = data;
        footer = (u16 *)((u32)data + len);
        data = (u16 *)((u32)data + packetLength);
        if (seqNoFlag == 1 ) {
            u16 *pCurrSeqNo = &(status->portSeqNo[aid][port & 0x0007 ]);
            u32 currSeqNo = *pCurrSeqNo;
            seqNo = *footer;
            footer++;
            if (currSeqNo & 1) {
                *pCurrSeqNo = (u16)(seqNo << 1);
            } else {
                seqNo <<= 1;
                if ((u16)(currSeqNo - seqNo) < (128 << 1)) {
                    ((void) 0) ;
                    continue;
                } else {
                    *pCurrSeqNo = (u16)seqNo;
                }
            }
        }
        if (destBmpFlag == 1 ) {
            u32 destBitmap;
            destBitmap = *footer;
            footer++;
            if (!(destBitmap & (1 << status->aid))) {
                ((void)0) ;
                continue;
            }
        }
        ((void)0) ;
        if (len > 0) {
            WMPortRecvCallback *cb_Port;
            cb_Port = (WMPortRecvCallback *)native_host_arm7_arm_038073f0();
            cb_Port->apiid = WM_APIID_PORT_RECV;
            cb_Port->errcode = WM_ERRCODE_SUCCESS;
            cb_Port->state = WM_STATECODE_PORT_RECV;
            cb_Port->port = (u16)port;
            cb_Port->recvBuf = recvBuf;
            cb_Port->data = contents;
            cb_Port->length = (u16)len;
            cb_Port->aid = aid;
            cb_Port->myAid = status->aid;
            cb_Port->seqNo = (u16)seqNo;
            {
                u16 parentSize = status->mp_parentSize;
                u16 childSize = status->mp_childSize;
                cb_Port->maxSendDataSize = (status->aid == 0) ? parentSize : childSize;
                cb_Port->maxRecvDataSize = (status->aid == 0) ? childSize : parentSize;
            }
            native_host_arm7_arm_038073a4(cb_Port);
        } else {
            ((void)0) ;
        }
    }
}

u16 native_host_arm7_main_027e7c20(u32 dataLength, u32 txop, u32 pollBitmap, u32 targetVCount)
{
    register s32 tmptt;
    u16 vcount;
    u32 pollCnt;
    u32 mp_time;
    if (txop & 0x8000) {
        txop &= 0x7fff;
    } else {
        txop = 96 + ((txop + 24 + 4) * 4 ) + 6;
    }
    pollCnt = native_host_arm7_arm_03803830(pollBitmap);
    mp_time = (u32)(96 + (28 + 4 + dataLength + 2) * 4 );
    mp_time += (((10 + 20) + 20) + 620) + txop * pollCnt + (10 + 96 + 32 * 4) ;
    vcount = (u16)GX_GetVCount();
    tmptt = (int)(targetVCount - 2 - vcount);
    while (tmptt < 0) {
        tmptt += 263;
    }
    tmptt *= 127;
#pragma optimize_for_size off
    tmptt /= 20;
    if (tmptt * 10 < mp_time) {
        tmptt = 0;
    }
    return (u16)tmptt;
}
