void native_host_arm7_main_027e72d4(u16 pollBitmap)
{
    WMSPWork *sys = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    u32 wlBuf[128];
    WlMaMpCfm *wlResult;
    u16 tmptt;
    u32 currPollBitmap;
    u16 currTsf;
    u32 wmHeader;
    u32 childBitmap;
    u32 mpReadyBitmap;
    int nextRecvBufSize;
    u16 recvSize;
    {
        OSIntrMode e = native_host_arm7_arm_037fdd00();
        childBitmap = status->child_bitmap;
        mpReadyBitmap = status->mp_readyBitmap;
        (void)native_host_arm7_arm_037fdd14(e);
    }
    currTsf = *(u16 *)((0x04808000) + 0x0F8) ;
    wmHeader = status->mp_prevWmHeader;
    currPollBitmap = (u32)(pollBitmap & status->child_bitmap);
    recvSize = status->mp_recvSize;
    nextRecvBufSize = WMSP_GetMPOneReceiveBufferSizeParent(recvSize, native_host_arm7_arm_03803830(currPollBitmap));
    if (status->mp_recvBufSize < nextRecvBufSize) {
        ((void)0)
            ;
        native_host_arm7_arm_037fc468(2);
        native_host_arm7_arm_027e1a54();
        return;
    }
    if (status->mp_count == 1 || status->mp_limitCount == 1) {
        tmptt = native_host_arm7_main_027e7c20(status->mp_prevDataLength, status->mp_prevTxop, currPollBitmap, status->mp_parentVCount);
        wmHeader |= 0x8000 ;
    } else {
        tmptt = 0;
        wmHeader &= ~0x8000 ;
    }
    ((void)0) ;
    wlResult = native_host_arm7_arm_027e2314((u16 *)wlBuf, 0x800c, 0, 0, (u16)currPollBitmap, tmptt, currTsf, 0, (u16)wmHeader, ((void *)0) );
}

static int
WmspMakePortPacket(u32 pollBitmap, u32 childBitmap, u32 mpReadyBitmap, u16 *wmHeader, u32 *destBitmap, u32 *dataLength)
{
    WMSPWork *sys = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    u32 maxSize = status->mp_sendSize;
    u16 *sendBuf = (u16 *)status->mp_sendBuf;
    int restSize;
    u32 portBitmap;
    u16 *write_p;
    BOOL firstPacket;
    BOOL isParent;
    u32 packetCount;
    u32 tmpDestBitmap;
    u32 tmpDataLength;
    BOOL destCheckFlag;
    u32 destBitmapMask;
    u32 reachableBitmap;
    ((void)0) ;
    if (status->mp_sendBufSize < WMSP_GetMPSendBufferSize((int)maxSize)) {
        ((void)0)
            ;
        return WM_ERRCODE_FAILED;
    }
    if (status->aid >= 15 + 1) {
        ((void)0) ;
        return WM_ERRCODE_FAILED;
    }
    if (status->state == WM_STATE_MP_PARENT) {
        isParent = 1 ;
    } else if (status->state == WM_STATE_MP_CHILD) {
        isParent = 0 ;
    } else {
        ((void)0) ;
        return WM_ERRCODE_FAILED;
    }
    *wmHeader = 0;
    *destBitmap = 0;
    *dataLength = 0;
    tmpDestBitmap = 0;
    tmpDataLength = 0;
    restSize = (s32)maxSize;
    packetCount = 0;
    if (restSize < 0) {
        return WM_ERRCODE_FAILED;
    }
    destBitmapMask = mpReadyBitmap;
    destCheckFlag = 1 ;
    if (isParent) {
        if (status->mp_current_minPollBmpMode) {
            destBitmapMask = childBitmap;
            destCheckFlag = 0 ;
        }
    } else {
        destCheckFlag = 0 ;
    }
    reachableBitmap = mpReadyBitmap & pollBitmap;
    portBitmap = 0;
    write_p = sendBuf;
    firstPacket = 1 ;
    native_host_arm7_arm_037fc888(&status->sendQueueMutex);
    if (status->sendQueueInUse == 1 ) {
        native_host_arm7_arm_037fc90c(&status->sendQueueMutex);
        return WM_ERRCODE_FAILED;
    }
    status->sendQueueInUse = 1 ;
    {
        WMPortSendQueueData *queueData = status->sendQueueData;
        u32 iPrio;
        for (iPrio = 0; iPrio < 4 && restSize > 2 ; iPrio++) {
            WMPortSendQueue *queue;
            WMPortSendQueue *sendQueue;
            u32 index;
            u16 *prevPointer;
            u32 prevIndex;
            queue = &(status->readyQueue[iPrio]);
            sendQueue = &(status->sendQueue[iPrio]);
            prevPointer = &queue->head;
            prevIndex = ((u16)0xffff) ;
            for (index = queue->head; index != ((u16)0xffff) && restSize > 2 ;
                index = (u16)((index != ((u16)0xffff) ) ? queueData[index].next : queue->head)) {
                WMPortSendQueueData *data = &(queueData[index]);
                u32 portBit;
                u32 currDestBitmap;
                u16 *contents;
                BOOL addSeqNoFlag, addDestBmpFlag;
                portBit = (1U << data->port);
                if ((portBitmap & portBit) != 0) {
                    goto next_packet;
                }
                portBitmap |= portBit;
                currDestBitmap = data->restBitmap & destBitmapMask;
                if (destCheckFlag && (currDestBitmap & ~reachableBitmap)) {
                    ((void) 0)
                        ;
                    goto next_packet;
                }
                addSeqNoFlag = (data->port & 0x0008 ) ? 1 : 0 ;
                addDestBmpFlag = (isParent && ((data->restBitmap | 1) != 0xffffU)) ? 1 : 0 ;
                if ((data->size & 1) == 1) {
                    ((void)0) ;
                    data->size++;
                }
                if (data->size + (firstPacket ? 0 : 2 ) + (addSeqNoFlag ? 2 : 0) + (addDestBmpFlag ? 2 : 0) <= restSize) {
                    if (firstPacket == 0 ) {
                        wmHeader = write_p;
                        *wmHeader = 0;
                        write_p++;
                        tmpDataLength += 2 ;
                        restSize -= 2 ;
                    }
                    *wmHeader |= ((data->port << 8 ) & 0x0f00 )
                        | ((data->size / 2 ) & 0x00ff );
                    contents = write_p;
                    MI_CpuCopy16(data->data, write_p, data->size);
                    write_p += data->size / sizeof(u16);
                    tmpDataLength += data->size;
                    restSize -= data->size;
                    if (addSeqNoFlag == 1 ) {
                        u32 seqNo;
                        if (data->seqNo & 1)
                        {
                            seqNo = status->portSeqNo[status->aid][data->port & 0x0007 ]++;
                            data->seqNo = (u16)(seqNo << 1);
                        } else {
                            seqNo = (u32)(data->seqNo >> 1U);
                        }
                        seqNo &= 0x7fffU;
                        *write_p = (u16)seqNo;
                        write_p++;
                        tmpDataLength += 2;
                        restSize -= 2;
                    }
                    if (addDestBmpFlag == 1 ) {
                        *wmHeader |= 0x1000 ;
                        *write_p = data->restBitmap;
                        write_p++;
                        tmpDataLength += 2;
                        restSize -= 2;
                    }
                    if (firstPacket == 1 ) {
                        firstPacket = 0 ;
                    }
                    if (queue->tail == index) {
                        ((void) 0) ;
                        queue->tail = (u16)prevIndex;
                    }
                    *prevPointer = data->next;
                    data->next = ((u16)0xffff) ;
                    if (sendQueue->tail == ((u16)0xffff) ) {
                        ((void) 0) ;
                        sendQueue->head = (u16)index;
                    } else {
                        ((void) 0) ;
                        queueData[sendQueue->tail].next = (u16)index;
                    }
                    sendQueue->tail = (u16)index;
                    ((void) 0) ;
                    data->sendingBitmap = (u16)currDestBitmap;
                    packetCount++;
                    portBitmap &= ~portBit;
                    tmpDestBitmap |= data->destBitmap;
                    index = prevIndex;
                    if (status->mp_current_singlePacketMode == 1 ) {
                        goto packet_found;
                    }
                } else {
                    ((void) 0)
                        ;
                }
next_packet:
                if (index != ((u16)0xffff) ) {
                    prevPointer = &(queueData[index].next);
                } else {
                    prevPointer = &queue->head;
                }
                prevIndex = index;
            }
        }
    }
packet_found:
    *destBitmap = tmpDestBitmap;
    *dataLength = tmpDataLength;
    native_host_arm7_arm_037fc90c(&status->sendQueueMutex);
    return WM_ERRCODE_SUCCESS;
}

int native_host_arm7_main_027e73c4(u32 childBitmap, u16 priority, u16 port, u32 destBitmap, const u16 *sendData, u16 sendDataSize, WMCallbackFunc callback, void *arg)
{
    WMSPWork *sys = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    WMPortSendQueueData *queueData = status->sendQueueData;
    WMPortSendQueue *queue = &status->readyQueue[priority];
    WMPortSendQueueData *newData;
    u16 newIndex;
    if (sendDataSize == 0) {
        ((void)0) ;
        return WM_ERRCODE_INVALID_PARAM;
    }
    if (sendDataSize + ((port & 0x0008 ) ? 2 : 0) > 0x204) {
        ((void)0) ;
        return WM_ERRCODE_INVALID_PARAM;
    }
    native_host_arm7_arm_037fc888(&status->sendQueueMutex);
    newIndex = status->sendQueueFreeList.head;
    if (newIndex == ((u16)0xffff) ) {
        native_host_arm7_arm_037fc90c(&status->sendQueueMutex);
        return WM_ERRCODE_SEND_QUEUE_FULL;
    }
    newData = &queueData[newIndex];
    status->sendQueueFreeList.head = newData->next;
    if (status->sendQueueFreeList.tail == newIndex) {
        ((void) 0) ;
        status->sendQueueFreeList.tail = ((u16)0xffff) ;
    }
    newData->port = port;
    newData->destBitmap = (u16)destBitmap;
    newData->restBitmap = (u16)(destBitmap & childBitmap);
    newData->sentBitmap = 0;
    newData->sendingBitmap = 0;
    newData->data = sendData;
    newData->size = sendDataSize;
    newData->callback = callback;
    newData->arg = arg;
    newData->next = ((u16)0xffff) ;
    newData->seqNo = 0xffffU;
    newData->retryCount = status->mp_current_defaultRetryCount;
    if (queue->tail == ((u16)0xffff) ) {
        ((void) 0) ;
        queue->head = newIndex;
    } else {
        ((void) 0) ;
        queueData[queue->tail].next = newIndex;
    }
    queue->tail = newIndex;
    native_host_arm7_arm_037fc90c(&status->sendQueueMutex);
    return WM_ERRCODE_OPERATING;
}

BOOL native_host_arm7_main_027e74f8(BOOL timeout, u16 pollBitmap)
{
    WMSPWork *sys = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    WMPortSendQueueData *queueData = status->sendQueueData;
    int iPrio;
    BOOL isParent;
    u32 childBitmap;
    u32 mpReadyBitmap;
    BOOL retryFlag = 0 ;
    ((void)0) ;
    if (status->state == WM_STATE_MP_PARENT) {
        isParent = 1 ;
    } else if (status->state == WM_STATE_MP_CHILD) {
        isParent = 0 ;
    } else {
        ((void)0) ;
        return 0 ;
    }
    native_host_arm7_arm_037fc888(&status->sendQueueMutex);
    if (status->sendQueueInUse == 0 ) {
        native_host_arm7_arm_037fc90c(&status->sendQueueMutex);
        return 0 ;
    }
    if (isParent) {
        OSIntrMode e = native_host_arm7_arm_037fdd00();
        childBitmap = status->child_bitmap;
        mpReadyBitmap = status->mp_readyBitmap;
        (void)native_host_arm7_arm_037fdd14(e);
    } else {
        childBitmap = 0x0001U;
        mpReadyBitmap = 0x0001U;
    }
    for (iPrio = 0; iPrio < 4 ; iPrio++) {
        WMPortSendQueue *queue;
        WMPortSendQueue tmpQueue;
        u32 index;
        u16 *prevPointer;
        u32 prevIndex;
        queue = &status->sendQueue[iPrio];
        prevPointer = &queue->head;
        prevIndex = ((u16)0xffff) ;
        tmpQueue.head = tmpQueue.tail = ((u16)0xffff) ;
        for (index = queue->head; index != ((u16)0xffff) ;
            index = ((index != ((u16)0xffff) ) ? queueData[index].next : queue->head)) {
            WMPortSendQueueData *data = &queueData[index];
            if ((data->restBitmap & ~childBitmap) != 0) {
                ((void)0)
                    ;
            }
            if (!timeout) {
                data->sentBitmap |= data->sendingBitmap & ~pollBitmap;
                data->restBitmap &= ~data->sentBitmap;
            }
            data->restBitmap &= childBitmap;
            data->sendingBitmap = 0;
            if (data->restBitmap != 0 && ((data->port & 0x0008 ) || (data->retryCount > 0))) {
                retryFlag = 1 ;
                if (data->retryCount > 0) {
                    data->retryCount--;
                }
                if (data->next == ((u16)0xffff) ) {
                    ((void) 0) ;
                    queue->tail = (u16)prevIndex;
                }
                *prevPointer = data->next;
                data->next = ((u16)0xffff) ;
                if (tmpQueue.tail == ((u16)0xffff) ) {
                    ((void) 0) ;
                    tmpQueue.head = (u16)index;
                } else {
                    ((void) 0) ;
                    queueData[tmpQueue.tail].next = (u16)index;
                }
                tmpQueue.tail = (u16)index;
            } else {
                WMPortSendCallback *cb_PortSend;
                cb_PortSend = (WMPortSendCallback *)native_host_arm7_arm_038073f0();
                cb_PortSend->apiid = WM_APIID_PORT_SEND;
                if (data->restBitmap == 0) {
                    cb_PortSend->errcode = WM_ERRCODE_SUCCESS;
                } else {
                    cb_PortSend->errcode = WM_ERRCODE_SEND_FAILED;
                }
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
                    ((void) 0) ;
                    queue->tail = (u16)prevIndex;
                }
                *prevPointer = data->next;
                data->next = ((u16)0xffff) ;
                if (status->sendQueueFreeList.tail == ((u16)0xffff) ) {
                    ((void) 0) ;
                    status->sendQueueFreeList.head = (u16)index;
                } else {
                    ((void) 0) ;
                    queueData[status->sendQueueFreeList.tail].next = (u16)index;
                }
                status->sendQueueFreeList.tail = (u16)index;
            }
            index = prevIndex;
            if (index != ((u16)0xffff) ) {
                prevPointer = &(queueData[index].next);
            } else {
                prevPointer = &queue->head;
            }
            prevIndex = index;
        }
        if (tmpQueue.tail != ((u16)0xffff) ) {
            ((void) 0) ;
            ((void) 0) ;
            queueData[tmpQueue.tail].next = status->readyQueue[iPrio].head;
            if (status->readyQueue[iPrio].tail == ((u16)0xffff) ) {
                ((void) 0) ;
                status->readyQueue[iPrio].tail = tmpQueue.tail;
            }
            status->readyQueue[iPrio].head = tmpQueue.head;
        }
    }
    status->sendQueueInUse = 0 ;
    native_host_arm7_arm_037fc90c(&status->sendQueueMutex);
    return retryFlag;
}
