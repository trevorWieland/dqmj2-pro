static void WmspIndicate(WlCmdReq *req)
{
    if (((void *)0) == WMSP_GetSystemWork()->wm7buf) {
        return;
    }
    if (WM_STATE_STOP == WMSP_GetStatusStructure()->state) {
        return;
    }
    switch (req->header.code) {
    case (0x0000 | 0x84) :
        WmspIndicateMlmeAuthenticate(req);
        break;
    case (0x0000 | 0x85) :
        WmspIndicateMlmeDeAuthenticate(req);
        break;
    case (0x0000 | 0x86) :
        WmspIndicateMlmeAssociate(req);
        break;
    case (0x0000 | 0x87) :
        WmspIndicateMlmeReAssociate(req);
        break;
    case (0x0000 | 0x88) :
        WmspIndicateMlmeDisAssociate(req);
        break;
    case (0x0000 | 0x8B) :
        WmspIndicateMlmeBeaconLost(req);
        break;
    case (0x0000 | 0x8C) :
        WmspIndicateMlmeBeaconSend(req);
        break;
    case (0x0000 | 0x8D) :
        WmspIndicateMlmeBeaconRecv(req);
        break;
    case (0x0100 | 0x80) :
        WmspIndicateMaData(req);
        break;
    case (0x0100 | 0x82) :
        WmspIndicateMaMultiPoll(req);
        break;
    case (0x0100 | 0x84) :
        WmspIndicateMaMultiPollEnd(req);
        break;
    case (0x0100 | 0x85) :
        WmspIndicateMaMultiPollAck(req);
        break;
    case (0x0100 | 0x86) :
        WmspIndicateMaFatalErr(req);
        break;
    default:
        WmspIndicateFuncDummy(req);
    }
    native_host_arm7_arm_027e1a08(req);
}

void native_host_arm7_arm_027e1a08(WlCmdReq *buf);

static void WmspIndicateFuncDummy(WlCmdReq *req)
{
    ((void)0) ;
    return;
}

static void WmspIndicateMlmeBeaconSend(WlCmdReq *req)
{
    if (WMSP_GetStatusStructure()->beaconIndicateFlag > 0) {
        WMStartParentCallback *callback = (WMStartParentCallback *)native_host_arm7_arm_038073f0();
        callback->apiid = WM_APIID_START_PARENT;
        callback->errcode = WM_ERRCODE_SUCCESS;
        callback->state = WM_STATECODE_BEACON_SENT;
        native_host_arm7_arm_038073a4(callback);
    }
}

static void WmspIndicateMlmeBeaconRecv(WlCmdReq *req)
{
    WMSPWork *const work = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    WlMlmeBeaconRecvInd *pInd = (WlMlmeBeaconRecvInd *)req;
    WMGameInfo *pGameInfo = (WMGameInfo *)&(pInd->gameInfo);
    u32 *buf;
    WMSP_AddRssiToRandomPool(native_host_arm7_arm_027e1a40(pInd->rssi));
    if ((WM_STATE_CHILD != status->state) && (WM_STATE_MP_CHILD != status->state)) {
        return;
    }
    if (status->curr_tgid != pGameInfo->tgid) {
        BOOL result;
        buf = native_host_arm7_arm_027e0700();
        if (buf == ((void *)0) ) {
            result = 0 ;
        } else {
            buf[0] = WM_APIID_AUTO_DISCONNECT;
            buf[1] = 0x0001;
            buf[2] = WM_DISCONNECT_REASON_TGID_CHANGED;
            ((void)0) ;
            result = native_host_arm7_arm_037fc6d4(&(WMSP_GetSystemWork()->requestQ),
                (OSMessage)buf,
                0 );
        }
        if (!result) {
            WMIndCallback *cb = (WMIndCallback *)native_host_arm7_arm_038073f0();
            cb->apiid = WM_APIID_INDICATION;
            cb->errcode = WM_ERRCODE_FIFO_ERROR;
            cb->state = WM_STATECODE_FIFO_ERROR;
            cb->reason = WM_APIID_AUTO_DISCONNECT;
            native_host_arm7_arm_038073a4(cb);
        }
        return;
    } else {
        if (WMSP_GetStatusStructure()->beaconIndicateFlag > 0) {
            WMBeaconRecvIndCallback *callback = (WMBeaconRecvIndCallback *)native_host_arm7_arm_038073f0();
            callback->apiid = WM_APIID_INDICATION;
            callback->errcode = WM_ERRCODE_SUCCESS;
            callback->state = WM_STATECODE_BEACON_RECV;
            callback->tgid = pGameInfo->tgid;
            callback->wmstate = status->state;
            callback->gameInfoLength = pInd->gameInfoLength;
            if (callback->gameInfoLength <= 128) {
                MI_CpuCopy16(pGameInfo,
                    &(callback->gameInfo),
                    ((callback->gameInfoLength + 1U) & ~1U));
            }
            native_host_arm7_arm_038073a4(callback);
        }
    }
}

static void WmspIndicateMlmeBeaconLost(WlCmdReq *req)
{
    if (WMSP_GetStatusStructure()->beaconIndicateFlag > 0) {
        WMStartConnectCallback *callback = (WMStartConnectCallback *)native_host_arm7_arm_038073f0();
        callback->apiid = WM_APIID_START_CONNECT;
        callback->errcode = WM_ERRCODE_SUCCESS;
        callback->state = WM_STATECODE_BEACON_LOST;
        native_host_arm7_arm_038073a4(callback);
    }
}

static void WmspIndicateMaMultiPollEnd(WlCmdReq *req)
{
    u16 i;
    WMStatus *status = WMSP_GetStatusStructure();
    WMStartMPCallback *callback;
    WlMaMpEndInd *pInd = (WlMaMpEndInd *)req;
    WMMpRecvHeader *bufp;
    WMMpRecvData *datap;
    OSIntrMode enabled;
    BOOL kick;
    BOOL retryFlag = 0 ;
    u32 size;
    OSTick now;
    u16 errBitmap;
    u32 recvErrorBitmap;
    if (status->mp_flag == 0 ) {
        return;
    }
    ((void)0) ;
    errBitmap = pInd->mpKey.errBitmap;
    if (errBitmap != 0 || (status->mp_resumeFlag == 1 && pInd->mpKey.bitmap != 0)) {
        if (errBitmap != 0) {
            ((void) 0) ;
        }
        native_host_arm7_arm_027e1a54();
        return;
    }
    if (status->mp_resumeFlag != 0 ) {
        status->mp_resumeFlag = 0 ;
    }
    bufp = (WMMpRecvHeader *)status->mp_recvBuf[status->mp_recvBufSel];
    size = pInd->mpKey.length * pInd->mpKey.count + sizeof(WMMpRecvHeader) - sizeof(WMMpRecvData);
    if (status->mp_recvBufSize < size) {
        ((void)0)
            ;
        size = status->mp_recvBufSize;
    }
    native_host_arm7_arm_037fe12c(&(pInd->mpKey),
        bufp,
        size
    );
    WmspSetRssi(pInd, bufp->bitmap, status->mp_minPollBmpMode);
    now = native_host_arm7_arm_037fd21c() | 1;
    datap = bufp->data;
    recvErrorBitmap = bufp->bitmap;
    for (i = 0; i < bufp->count; ++i, datap = (WMMpRecvData *)(((u32)datap) + bufp->length)) {
        u16 aid = datap->aid;
        u16 length = datap->length;
        if (aid < 1 || 15 < aid) {
            continue;
        }
        if (length >= 2 && length != 0xffff) {
            datap->length -= 2;
            length -= 2;
            status->mp_readyBitmap |= (1 << aid);
            status->mp_lastRecvTick[aid] = now;
            if (length != 0) {
                native_host_arm7_arm_027e7a1c(aid, datap->wmHeader, datap->cdata, length, (WMMpRecvBuf *)bufp);
            }
        } else if (length == 0) {
            OSTick last = status->mp_lastRecvTick[aid];
            recvErrorBitmap |= (1 << aid);
            if (status->mp_lifeTimeTick != 0ULL && last != 0ULL
                && (now - last) > status->mp_lifeTimeTick) {
                u32 *buf = native_host_arm7_arm_027e0700();
                BOOL result;
                ((void) 0) ;
                status->mp_lastRecvTick[aid] = 0ULL;
                if (buf == ((void *)0) ) {
                    result = 0 ;
                } else {
                    buf[0] = WM_APIID_AUTO_DISCONNECT;
                    buf[1] = (u32)(1 << aid);
                    buf[2] = WM_DISCONNECT_REASON_MP_LIFETIME;
                    ((void)0) ;
                    result = native_host_arm7_arm_037fc6d4(&(WMSP_GetSystemWork()->requestQ),
                        (OSMessage)buf,
                        0 );
                }
                if (!result) {
                    WMIndCallback *cb = (WMIndCallback *)native_host_arm7_arm_038073f0();
                    cb->apiid = WM_APIID_INDICATION;
                    cb->errcode = WM_ERRCODE_FIFO_ERROR;
                    cb->state = WM_STATECODE_FIFO_ERROR;
                    cb->reason = WM_APIID_AUTO_DISCONNECT;
                    native_host_arm7_arm_038073a4(cb);
                }
            }
        }
    }
    (void)native_host_arm7_arm_027e74f8(0 , (u16)recvErrorBitmap);
    if (bufp->bitmap != 0) {
        retryFlag = 1 ;
    }
    callback = (WMStartMPCallback *)native_host_arm7_arm_038073f0();
    callback->apiid = WM_APIID_START_MP;
    callback->errcode = WM_ERRCODE_SUCCESS;
    callback->state = WM_STATECODE_MPEND_IND;
    callback->recvBuf = (WMMpRecvBuf *)bufp;
    native_host_arm7_arm_038073a4(callback);
    status->mp_recvBufSel ^= 1;
    enabled = native_host_arm7_arm_037fdd00();
    if (retryFlag == 0 ) {
        status->mp_count--;
    }
    if (status->mp_limitCount > 0) {
        status->mp_limitCount--;
    }
    kick = (status->mp_count > 0 && status->mp_limitCount > 0);
    (void)native_host_arm7_arm_037fdd14(enabled);
    if (kick) {
        u16 pollbmp;
        if (retryFlag == 1 ) {
            pollbmp = pInd->mpKey.bitmap;
        } else {
            pollbmp = 0xffff;
        }
        if (status->mp_parentInterval != 0) {
            WmspCancelMPIntervalAlarm();
            native_host_arm7_arm_037fd4dc(
                &native_host_arm7_data_0380b490,
                status->mp_parentIntervalTick,
                native_host_arm7_arm_027e1ad4,
                (void *)pollbmp);
        } else {
            native_host_arm7_arm_027e1ae8(pollbmp);
        }
    }
    ((void)0) ;
}

void native_host_arm7_arm_027e1a54(void);

void native_host_arm7_arm_027e1ad4(void *arg);

void native_host_arm7_arm_027e1ae8(u16 pollbmp);

static void WmspSetRssi(WlMaMpEndInd *pInd, u16 pollBitmap, BOOL minPollBmpMode)
{
    WlMpKeyData *kd;
    s32 i;
    u16 temp;
    u16 min;
    WMStatus *status = WMSP_GetStatusStructure();
    min = status->minRssi;
    if (pollBitmap != 0) {
        return;
    } else if (pInd->mpKey.count < 1) {
        return;
    } else {
        for (i = 0; i < pInd->mpKey.count; i++) {
            kd = (WlMpKeyData *)((u32)pInd->mpKey.data + (pInd->mpKey.length * i));
            temp = native_host_arm7_arm_027e1a40(kd->rssi);
            if (temp < min) {
                min = temp;
            }
        }
    }
    status->minRssi = min;
}

static void WmspIndicateMaMultiPoll(WlCmdReq *req)
{
    WMStartMPCallback *callback;
    WlMaMpInd *pInd = (WlMaMpInd *)req;
    WMSPWork *sys = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    WMMpRecvBuf *bufp;
    OSIntrMode enabled;
    BOOL timeout;
    u16 oldSentFlag, oldEmptyFlag;
    BOOL polled;
    u32 size;
    u16 txKeySts;
    {
        u16 rssi8;
        rssi8 = native_host_arm7_arm_027e1a40(pInd->frame.rssi);
        if (status->minRssi > rssi8) {
            status->minRssi = rssi8;
        }
    }
    if (status->mp_flag == 0 ) {
        return;
    }
    ((void)0)        ;
    if (status->mp_vsyncFlag == 1 ) {
        ((void) 0) ;
        status->mp_vsyncFlag = 0 ;
    }
    oldEmptyFlag = status->mp_bufferEmptyFlag;
    oldSentFlag = status->mp_sentDataFlag;
    status->mp_recvBufSel ^= 1;
    bufp = status->mp_recvBuf[status->mp_recvBufSel];
    size = pInd->frame.length + sizeof(WMMpRecvBuf) - 6U;
    if (status->mp_recvBufSize < size) {
        ((void)0)
            ;
        size = status->mp_recvBufSize;
    }
    native_host_arm7_arm_037fe12c(&(pInd->frame),
        bufp,
        size
    );
    enabled = native_host_arm7_arm_037fdd00();
    timeout = 0 ;
    if (status->mp_waitAckFlag == 1 ) {
        timeout = 1 ;
        WmspCancelMPAckAlarm();
        ((void) 0) ;
    }
    status->mp_waitAckFlag = 1 ;
    status->mp_ackTime = bufp->ackTimeStamp;
    txKeySts = pInd->frame.txKeySts;
    polled = ((txKeySts & (0x0001 << 13) ) ? 1 : 0 );
    status->mp_isPolledFlag = (u16)polled;
    native_host_arm7_arm_037fd4dc(
        &native_host_arm7_data_0380b464,
        ((OSTick)(((33514000 / 1000) * (u64)(((u16)(bufp->ackTimeStamp - bufp->timeStamp) + 128) << 4)) / 64)) / 1024,
        native_host_arm7_arm_027e1b68,
        ((void *)0) );
    {
        BOOL sent, empty;
        empty = ((txKeySts & ((0x0001 << 13) | (0x0001 << 11) )) == ((0x0001 << 13) | (0x0001 << 11) ));
        sent = ((txKeySts & ((0x0001 << 13) | (0x0001 << 14) )) == ((0x0001 << 13) | (0x0001 << 14) ));
        if (sent) {
            status->mp_setDataFlag = 0 ;
        }
        status->mp_bufferEmptyFlag = (u16)((empty) ? 1 : 0 );
        status->mp_sentDataFlag = (u16)((sent) ? 1 : 0 );
    }
    if (polled) {
        s32 childSize;
        childSize = ((((s32)bufp->txop - 96 - 6) / 4) - 24 - 4 - 2 - 2 );
        if (childSize >= 0) {
            if (childSize > 0x200) {
                childSize = 0x200;
            }
            if (childSize != status->mp_childSize) {
                ((void)0) ;
                native_host_arm7_arm_027e086c((u16)childSize);
            }
        }
    }
    (void)native_host_arm7_arm_037fdd14(enabled);
    if (timeout) {
        if (oldEmptyFlag == 1 ) {
            (void)native_host_arm7_arm_027e74f8(timeout, 0x0000);
        }
        callback = (WMStartMPCallback *)native_host_arm7_arm_038073f0();
        callback->apiid = WM_APIID_START_MP;
        callback->errcode = WM_ERRCODE_TIMEOUT;
        callback->state = WM_STATECODE_MPACK_IND;
        callback->recvBuf = ((void *)0) ;
        native_host_arm7_arm_038073a4(callback);
    }
    if (!polled) {
        if (bufp->length >= 2) {
            status->mp_vsyncOrderedFlag = ((bufp->wmHeader & 0x8000 ) != 0);
        }
        ((void)0) ;
        return;
    }
    native_host_arm7_arm_037fe12c(pInd->frame.destAdrs, bufp->destAdrs, 6 );
    native_host_arm7_arm_037fe12c(pInd->frame.srcAdrs, bufp->srcAdrs, 6 );
    if (bufp->length >= 2) {
        bufp->length -= 2;
        status->mp_vsyncOrderedFlag = ((bufp->wmHeader & 0x8000 ) != 0);
        callback = (WMStartMPCallback *)native_host_arm7_arm_038073f0();
        callback->apiid = WM_APIID_START_MP;
        callback->errcode = WM_ERRCODE_SUCCESS;
        callback->state = WM_STATECODE_MP_IND;
        callback->recvBuf = bufp;
        native_host_arm7_arm_038073a4(callback);
        if (bufp->length > 0) {
            native_host_arm7_arm_027e7a1c(0, bufp->wmHeader, bufp->data, bufp->length, bufp);
        }
    } else {
        bufp->length = 0;
        status->mp_vsyncOrderedFlag = 0 ;
        callback = (WMStartMPCallback *)native_host_arm7_arm_038073f0();
        callback->apiid = WM_APIID_START_MP;
        callback->errcode = WM_ERRCODE_NO_DATA;
        callback->state = WM_STATECODE_MP_IND;
        callback->recvBuf = bufp;
        native_host_arm7_arm_038073a4(callback);
    }
    if (status->mp_lifeTimeTick != 0ULL) {
        status->mp_lastRecvTick[0] = native_host_arm7_arm_037fd21c() | 1;
    }
    ((void)0) ;
}

void native_host_arm7_arm_027e1b68(void *arg);
