u16 DEV_TestRxReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt)
{
    WlDevTestRxReq *pReq = (WlDevTestRxReq *)pReqt;
    WlDevTestRxCfm *pCfm = (WlDevTestRxCfm *)pCfmt;
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    pCfm->header.length = ((sizeof(WlDevTestRxCfm) - sizeof(WlCmdHeader) + 1) / 2) ;
    if ((pWork->STA & 0xF0 ) != 0x10 ) {
        return 0x01 ;
    }
    switch (pReq->control) {
    case 1 :
        if (pWork->STA != 0x10 ) {
            return 0x01 ;
        }
        WSetChannel(pReq->channel, 1 );
        pWork->Mode = 0 ;
        WStart();
        WSetForcePowerState(((0x0000 << 0) | (0x0001 << 15)) );
        pWork->STA = 0x11 ;
        break;
    case 0 :
        if (pWork->STA == 0x11 ) {
            WSetForcePowerState((0x0000 << 15) );
            WStop();
        } else {
            return 0x01 ;
        }
        pWork->STA = 0x10 ;
        break;
    }
    return 0x00 ;
}
