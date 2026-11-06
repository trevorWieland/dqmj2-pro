static void WmspIndicateMaMultiPollAck(WlCmdReq *req)
{
    WMstartMPCallback *callback;
    WlMaMpAckInd *pInd = (WlMaMpAckInd *)req;
    WlRxMpAckFrame *pFrame = (WlRxMpAckFrame *)&(pInd->ack);
    WMSPWork *sys = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    OSIntrMode enabled;
    BOOL failed;
    BOOL timeout;
    BOOL retryFlag = 0 ;
    BOOL sent, empty;
    BOOL polled;
    u16 timeStamp;
    if (status->mp_flag == 0 ) {
        return;
    }
    if (pInd->header.length == 0) {
        u16 lower0, lower1;
        u16 higher;
        timeout = 1 ;
        lower0 = *(vu16 *)((0x04808000) + 0x0F8) ;
        higher = *(vu16 *)((0x04808000) + 0x0FA) ;
        lower1 = *(vu16 *)((0x04808000) + 0x0F8) ;
        if (lower0 > lower1) {
            higher = *(vu16 *)((0x04808000) + 0x0FA) ;
        }
        timeStamp = (u16)((higher << (16 - 4)) | (lower1 >> 4));
        if (!((s16)(timeStamp - status->mp_ackTime) > 0)) {
            ((void) 0) ;
            return;
        }
    } else {
        timeout = 0 ;
    }
    enabled = native_host_arm7_arm_037fdd00();
    if (status->mp_waitAckFlag == 0 ) {
        (void)native_host_arm7_arm_037fdd14(enabled);
        ((void)0)
            ;
        return;
    }
    status->mp_waitAckFlag = 0 ;
    polled = status->mp_isPolledFlag;
    WmspCancelMPAckAlarm();
    (void)native_host_arm7_arm_037fdd14(enabled);
    sent = status->mp_sentDataFlag;
    failed = !sent || (!timeout && (pFrame->bitmap & (1 << status->aid)));
    if (status->mp_sentDataFlag) {
        status->mp_sentDataFlag = 0 ;
    }
    empty = status->mp_bufferEmptyFlag;
    if (empty) {
        status->mp_bufferEmptyFlag = 0 ;
        retryFlag = native_host_arm7_arm_027e74f8(timeout, (u16)((failed) ? 0x0001 : 0x0000));
    }
    ((void)0) ;
    if (!polled) {
        ((void)0) ;
        return;
    }
    callback = (WMStartMPCallback *)native_host_arm7_arm_038073f0();
    callback->apiid = WM_APIID_START_MP;
    if (timeout) {
        callback->errcode = WM_ERRCODE_TIMEOUT;
    } else if (pFrame->bitmap & (1 << status->aid)) {
        callback->errcode = WM_ERRCODE_SEND_FAILED;
    } else {
        callback->errcode = WM_ERRCODE_SUCCESS;
    }
    callback->state = WM_STATECODE_MPACK_IND;
    callback->recvBuf = ((void *)0) ;
    if (!timeout) {
        callback->timeStamp = pFrame->timeStamp;
        callback->rate_rssi = *(u16 *)&(pFrame->rate);
        native_host_arm7_arm_037fe12c(pFrame->destAdrs, callback->destAdrs, 6 );
        native_host_arm7_arm_037fe12c(pFrame->srcAdrs, callback->srcAdrs, 6 );
        callback->seqNum = pFrame->seqCtrl;
        callback->tmptt = pFrame->tmptt;
        callback->pollbmp = pFrame->bitmap;
    }
    native_host_arm7_arm_038073a4(callback);
    ((void)0) ;
    if (polled) {
        if (retryFlag == 1 || status->mp_vsyncOrderedFlag == 0 ) {
            if (status->mp_childInterval != 0) {
                WmspCancelMPIntervalAlarm();
                native_host_arm7_arm_037fd4dc(
                    &native_host_arm7_data_0380b490,
                    status->mp_childIntervalTick,
                    native_host_arm7_arm_027e1c00,
                    ((void *)0) );
            } else {
                native_host_arm7_arm_027e1c0c();
            }
        } else {
            status->mp_vsyncOrderedFlag = 0 ;
            status->mp_vsyncFlag = 1 ;
            status->mp_newFrameFlag = 0 ;
        }
    }
}

void native_host_arm7_arm_027e1c00(void *arg);

void native_host_arm7_arm_027e1c0c(void);

static void WmspIndicateMaData(WlCmdReq *req)
{
    WMStartDCFCallback *callback;
    WlMaDataInd *pInd = (WlMaDataInd *)req;
    WMStatus *status = WMSP_GetStatusStructure();
    WlRxFrame *pFrame;
    WMDcfRecvBuf *bufp;
    if (status->dcf_flag == 0 ) {
        return;
    }
    {
        WMSPWork *pw = WMSP_GetSystemWork();
        native_host_arm7_arm_027e0520(native_host_arm7_arm_027e1a40(pInd->frame.rssi));
        status->linkLevel = native_host_arm7_arm_027e059c();
    }
    pFrame = (WlRxFrame *)&pInd->frame;
    if (1 == native_host_arm7_arm_027e02ac((u8 *)(pFrame->srcAdrs))) {
        return;
    }
    if (pFrame->length > 1508 ) {
        return;
    }
    status->dcf_recvBufSel ^= 1;
    bufp = status->dcf_recvBuf[status->dcf_recvBufSel];
    native_host_arm7_arm_037fe12c(pFrame,
        bufp,
        (pFrame->length + 44 + 1U) & ~1U
    );
    native_host_arm7_arm_037fe12c(pFrame->destAdrs, bufp->destAdrs, 6 );
    native_host_arm7_arm_037fe12c(pFrame->srcAdrs, bufp->srcAdrs, 6 );
    callback = (WMStartDCFCallback *)native_host_arm7_arm_038073f0();
    callback->apiid = WM_APIID_START_DCF;
    callback->errcode = WM_ERRCODE_SUCCESS;
    callback->state = WM_STATECODE_DCF_IND;
    callback->recvBuf = bufp;
    native_host_arm7_arm_038073a4(callback);
}

static void WmspIndicateMaFatalErr(WlCmdReq *req)
{
    WlMaFatalErrInd *pInd = (WlMaFatalErrInd *)req;
    u32 *buf;
    BOOL result;
    WMSPWork *sys = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    ((void)0) ;
    if (status->mp_current_ignoreFatalErrorMode == 1 && pInd->errCode == 0x20) {
        ((void)0) ;
        {
            OSIntrMode enabled;
            enabled = native_host_arm7_arm_037fdd00();
            WmspCancelMPAckAlarm();
            status->mp_waitAckFlag = 0 ;
            (void)native_host_arm7_arm_037fdd14(enabled);
            status->mp_setDataFlag = 0 ;
            (void)native_host_arm7_arm_027e74f8(1 , 0x0000);
        }
        {
            WMIndCallback *cb = (WMIndCallback *)native_host_arm7_arm_038073f0();
            cb->apiid = WM_APIID_INDICATION;
            cb->errcode = WM_ERRCODE_SUCCESS;
            cb->state = WM_STATECODE_INFORMATION;
            cb->reason = WM_INFOCODE_FATAL_ERROR;
            native_host_arm7_arm_038073a4(cb);
        }
    } else {
        buf = native_host_arm7_arm_027e0700();
        if (buf == ((void *)0) ) {
            result = 0 ;
        } else {
            buf[0] = WM_APIID_AUTO_DISCONNECT;
            buf[2] = WM_DISCONNECT_REASON_FATAL_ERROR;
            if (WMSPi_IsParent(status->state)) {
                buf[1] = 0x7ffe;
            } else if (WMSPi_IsChild(status->state)) {
                buf[1] = 0x0001;
            }
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

static void WmspIndicateMlmeDisAssociate(WlCmdReq *req)
{
    WMIndCallback *callback = (WMIndCallback *)native_host_arm7_arm_038073f0();
    callback->apiid = WM_APIID_INDICATION;
    callback->errcode = WM_ERRCODE_SUCCESS;
    callback->state = WM_STATECODE_DISASSOCIATE;
    native_host_arm7_arm_038073a4(callback);
}

static void WmspIndicateMlmeReAssociate(WlCmdReq *req)
{
    WMIndCallback *callback = (WMIndCallback *)native_host_arm7_arm_038073f0();
    callback->apiid = WM_APIID_INDICATION;
    callback->errcode = WM_ERRCODE_SUCCESS;
    callback->state = WM_STATECODE_REASSOCIATE;
    native_host_arm7_arm_038073a4(callback);
}

static void WmspIndicateMlmeAssociate(WlCmdReq *req)
{
    WlMlmeAssInd *pInd = (WlMlmeAssInd *)req;
    WMStatus *status = WMSP_GetStatusStructure();
    WMStartParentCallback *callback;
    u32 *buf;
    u32 aid;
    aid = pInd->aid;
    if (aid == 0 || aid >= (15 + 1)) {
        ((void)0) ;
        return;
    }
    if (!status->pparam.entryFlag) {
        BOOL result;
        buf = native_host_arm7_arm_027e0700();
        if (buf == ((void *)0) ) {
            result = 0 ;
        } else {
            buf[0] = WM_APIID_AUTO_DEAUTH;
            native_host_arm7_arm_037fe12c(pInd->peerMacAdrs, &buf[1], 6);
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
            cb->reason = WM_APIID_AUTO_DEAUTH;
            native_host_arm7_arm_038073a4(cb);
        }
        return;
    }
    {
        OSIntrMode e = native_host_arm7_arm_037fdd00();
        status->child_bitmap |= (0x0001 << aid);
        status->mp_readyBitmap &= ~(0x0001 << aid);
        status->mp_lastRecvTick[aid] = native_host_arm7_arm_037fd21c() | 1;
        native_host_arm7_arm_037fe12c(pInd->peerMacAdrs, status->childMacAddress[aid - 1], 6 );
        (void)native_host_arm7_arm_037fdd14(e);
    }
    MI_CpuFill16(status->portSeqNo[aid], 0x0001, sizeof(status->portSeqNo[0]));
    callback = (WMStartParentCallback *)native_host_arm7_arm_038073f0();
    callback->apiid = WM_APIID_START_PARENT;
    callback->errcode = WM_ERRCODE_SUCCESS;
    callback->state = WM_STATECODE_CONNECTED;
    native_host_arm7_arm_037fe12c(pInd->peerMacAdrs, callback->macAddress, 6 );
    callback->aid = (u16)aid;
    MI_CpuCopy16(&(pInd->ssid[8]), callback->ssid, 24 );
    callback->parentSize = status->mp_parentSize;
    callback->childSize = status->mp_childSize;
    native_host_arm7_arm_038073a4(callback);
}

static void WmspIndicateMlmeDeAuthenticate(WlCmdReq *req)
{
    int i;
    WMStatus *status = WMSP_GetStatusStructure();
    WlMlmeDeAuthInd *pInd = (WlMlmeDeAuthInd *)req;
    u8 tmpMacAddress[6];
    u16 tmpAID;
    if (WM_STATE_PARENT == status->state || WM_STATE_MP_PARENT == status->state) {
        native_host_arm7_arm_037fe12c(pInd->peerMacAdrs, tmpMacAddress, 6 );
        tmpAID = 0;
        for (i = 0; i < 15; ++i) {
            OSIntrMode e = native_host_arm7_arm_037fdd00();
            if ((status->child_bitmap & (0x0001 << (i + 1))) && status->childMacAddress[i][0] == tmpMacAddress[0] && status->childMacAddress[i][1] == tmpMacAddress[1] && status->childMacAddress[i][2] == tmpMacAddress[2] && status->childMacAddress[i][3] == tmpMacAddress[3] && status->childMacAddress[i][4] == tmpMacAddress[4] && status->childMacAddress[i][5] == tmpMacAddress[5]) {
                tmpAID = (u16)(i + 1);
                {
                    status->child_bitmap &= ~(0x0001 << tmpAID);
                    status->mp_readyBitmap &= ~(0x0001 << tmpAID);
                    status->mp_lastRecvTick[tmpAID] = 0ULL;
                }
                MI_CpuClear8(status->childMacAddress[i], 6 );
                (void)native_host_arm7_arm_037fdd14(e);
                break;
            }
            (void)native_host_arm7_arm_037fdd14(e);
        }
        if (tmpAID == 0) {
            return;
        } else {
            WMStartParentCallback *callback = (WMStartParentCallback *)native_host_arm7_arm_038073f0();
            callback->apiid = WM_APIID_START_PARENT;
            callback->errcode = WM_ERRCODE_SUCCESS;
            callback->state = WM_STATECODE_DISCONNECTED;
            callback->reason = pInd->reasonCode;
            callback->aid = tmpAID;
            native_host_arm7_arm_037fe12c(pInd->peerMacAdrs, callback->macAddress, 6 );
            callback->parentSize = status->mp_parentSize;
            callback->childSize = status->mp_childSize;
            native_host_arm7_arm_038073a4(callback);
            if (status->mp_flag == 1 ) {
                native_host_arm7_arm_027e7828((u16)(0x0001 << tmpAID));
            }
        }
    } else {
        BOOL fCleanQueue = 0 ;
        OSIntrMode e = native_host_arm7_arm_037fdd00();
        if (status->child_bitmap == 0) {
            (void)native_host_arm7_arm_037fdd14(e);
            return;
        }
        if (status->mp_flag == 1 ) {
            status->mp_flag = 0 ;
            fCleanQueue = 1 ;
            native_host_arm7_arm_027e5b98();
            native_host_arm7_arm_027e0640();
        }
        status->child_bitmap = 0;
        status->mp_readyBitmap = 0;
        status->ks_flag = 0 ;
        status->dcf_flag = 0 ;
        status->VSyncFlag = 0 ;
        status->wep_flag = 0 ;
        status->wepMode = 0 ;
        MI_CpuClear8(status->wepKey, 80 );
        native_host_arm7_arm_027e076c();
        status->beaconIndicateFlag = 0;
        status->state = WM_STATE_CLASS1;
        (void)native_host_arm7_arm_037fdd14(e);
        {
            WMStartConnectCallback *callback = (WMStartConnectCallback *)native_host_arm7_arm_038073f0();
            callback->apiid = WM_APIID_START_CONNECT;
            callback->errcode = WM_ERRCODE_SUCCESS;
            callback->state = WM_STATECODE_DISCONNECTED;
            callback->reason = pInd->reasonCode;
            callback->aid = status->aid;
            native_host_arm7_arm_037fe12c(status->parentMacAddress, callback->macAddress, 6 );
            callback->parentSize = status->mp_parentSize;
            callback->childSize = status->mp_childSize;
            native_host_arm7_arm_038073a4(callback);
        }
        if (fCleanQueue) {
            native_host_arm7_arm_027e7828(0x0001);
        }
    }
}

static void WmspIndicateMlmeAuthenticate(WlCmdReq *req)
{
    WMIndCallback *callback = (WMIndCallback *)native_host_arm7_arm_038073f0();
    callback->apiid = WM_APIID_INDICATION;
    callback->errcode = WM_ERRCODE_SUCCESS;
    callback->state = WM_STATECODE_AUTHENTICATE;
    native_host_arm7_arm_038073a4(callback);
}
