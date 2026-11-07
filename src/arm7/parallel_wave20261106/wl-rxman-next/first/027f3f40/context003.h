static void RxReAssResFrame(LPREASSRES_FRAME pFrm)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    LPMLME_MAN pMLME = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->MLME;
    LPREASSRES_BODY pReAssRes;
    u32 bodyLen;
    bodyLen = pFrm->FirmHeader.Length;
    pReAssRes = &pFrm->Body;
    ;
    if ((pWork->Mode != 2 ) && (pWork->Mode != 3 )) {
        ;
        return;
    }
    if (pMLME->State == (0x01 | 0x60) ) {
        if (native_host_arm7_arm_027ea480(pMLME->pReq.ReAss->newApMacAdrs, pFrm->Dot11Header.SA)) {
            native_host_arm7_arm_027eabec();
            if (pReAssRes->StatusCode == 0 ) {
                native_host_arm7_arm_027ea00c(pReAssRes->AID & 0x0FFF);
                native_host_arm7_arm_027f1f5c(pWork->AID);
                native_host_arm7_arm_027ea0ec(pWork->LinkAdrs, pFrm->Dot11Header.SA);
                pWork->APCamAdrs = native_host_arm7_arm_027eb90c(pFrm->Dot11Header.SA);
                native_host_arm7_arm_027ebc50(pWork->APCamAdrs, 0x40 );
                native_host_arm7_arm_037f9238(0x40 );
            }
            if (pReAssRes->StatusCode == 0x00 ) {
                pMLME->pCfm.ReAss->resultCode = 0x00 ;
                pMLME->pCfm.ReAss->statusCode = 0x00 ;
                native_host_arm7_arm_037f9238(0x40 );
            } else {
                pMLME->pCfm.ReAss->resultCode = 0x0C ;
                pMLME->pCfm.ReAss->statusCode = pReAssRes->StatusCode;
            }
            pMLME->pCfm.ReAss->aid = pWork->AID;
            pMLME->State = (0x03 | 0x60) ;
            native_host_arm7_arm_037f8598(2 , 4 );
        }
    }
}

void native_host_arm7_arm_027f3148(LPPRBREQ_FRAME pFrm);

void native_host_arm7_arm_027f31fc(LPPRBRES_FRAME pFrm, LPELEMENT_CHECKER pChk);

void native_host_arm7_arm_027f35cc(LPAUTH_FRAME pFrm);

void native_host_arm7_arm_027f3b6c(LPDEAUTH_FRAME pFrm);

static void RxPsPollFrame(LPPSPOLL_FRAME pFrm)
{
    LPHEAP_MAN pHeapMan = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->HeapMan;
    u32 cam_adrs;
    ;
    cam_adrs = pFrm->FirmHeader.CamAdrs;
    if (native_host_arm7_arm_027ebfec(cam_adrs) == 0x40 ) {
        native_host_arm7_arm_027ebdf4(cam_adrs);
        if (((*(LPHEAPBUF_MAN)&pHeapMan->TxPri[1]).Count) != 0) {
            native_host_arm7_arm_027eff00(1 );
        }
        if (((*(LPHEAPBUF_MAN)&pHeapMan->TxPri[0]).Count) != 0) {
            native_host_arm7_arm_027eff00(0 );
        }
    }
}

static void RxCfEndFrame(LPCFEND_FRAME pFrm)
{
    ;
}

void native_host_arm7_arm_027f3c1c(LPELEMENT_CHECKER p);
